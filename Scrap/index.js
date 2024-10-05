const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const axios = require("axios");
const { connectToDB, insertTopic, updateTopicWithChildren } = require("./mong");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

let db;

// Connect to MongoDB
connectToDB()
  .then((database) => {
    db = database;
  })
  .catch((err) => {
    console.error("Failed to connect to database:", err);
  });

// Route to get topics
app.get("/getTopics", async (req, res) => {
  try {
    const topics = await db.collection("topics").find({}).toArray();
    res.json(topics);
  } catch (error) {
    console.error("Error fetching topics:", error);
    res.status(500).json({ error: "Failed to fetch topics" });
  }
});

// Route to generate content for a child topic
app.post("/generateContentForChild", async (req, res) => {
  const { parentId, childId } = req.body;

  // Fetch the child topic based on childId
  const childTopic = await db
    .collection("topics")
    .findOne({ "child._id": childId });

  if (!childTopic) {
    return res.status(404).json({ error: "Child topic not found." });
  }

  const prompt = `Explain ${
    childTopic.child.find((c) => c._id === childId).name
  } in detail.`;

  try {
    const response = await axios.post("http://localhost:11434/api/generate", {
      model: "llama3.2",
      prompt,
      stream: false, // Ensuring the stream is off
    });

    const content = response.data.response;

    // Update the content for the clicked child topic in the database
    await updateTopicWithChildren(db, parentId, childId, content);

    res.json({ content });
  } catch (error) {
    console.error("Error generating content:", error);
    res.status(500).json({ error: "Failed to generate content" });
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
