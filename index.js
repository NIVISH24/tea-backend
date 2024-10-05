const express = require("express");
const { generateFromLLM } = require("./llm");
const cors = require("cors");
const {
  connectToDB,
  insertTopic,
  updateTopicWithChildren,
  ObjectId,
} = require("./mong");

const app = express();
const port = 3000;

app.use(cors()); // Add this line to enable CORS
app.use(express.json());

// Initialize MongoDB connection
let db;
connectToDB().then((database) => {
  db = database;
});

app.get("/getTopics", async (req, res) => {
  try {
    const topics = await db.collection("topics").find({}).toArray();
    res.status(200).json(topics);
  } catch (error) {
    console.error("Error fetching topics:", error);
    res.status(500).send("Error fetching topics");
  }
});

app.post("/generateContentForChild", async (req, res) => {
  const { parentId, childId } = req.body;

  try {
    // Fetch the parent topic from the database
    const parentTopic = await db
      .collection("topics")
      .findOne({ _id: new ObjectId(parentId) });
    if (!parentTopic) {
      return res.status(404).send("Parent topic not found");
    }

    // Find the specific child topic within the parent
    const childTopic = parentTopic.child.find((topic) =>
      topic.id.equals(childId)
    );
    if (!childTopic) {
      return res.status(404).send("Child topic not found");
    }

    // Generate content for the child topic
    const contentPrompt = `Generate detailed content with examples for the topic: "${childTopic.name}" suitable for an undergraduate student.`;

    const generatedContent = await generateFromLLM(contentPrompt);
    console.log("Generated content for child topic:", generatedContent);

    // Update the child topic with the generated content in the database
    await db
      .collection("topics")
      .updateOne(
        { _id: new ObjectId(parentId), "child.id": new ObjectId(childId) },
        { $set: { "child.$.content": generatedContent } }
      );

    res.status(200).send({ content: generatedContent });
  } catch (error) {
    console.error("Error generating content for child topic:", error);
    res.status(500).send("Error generating content for child topic");
  }
});

// Route to handle adding a prompt and generating topics/subheadings
app.post("/addPrompt", async (req, res) => {
  const { prompt } = req.body;

  try {
    // Step 1: Generate topic name and structure
    const topicPrompt = `Generate a structured JSON response in the following format for the user prompt: "${prompt}": 
      {name:"<Formal topic name Main Heading based on User Prompt>", child: [{name: "<topic_name>", child: [{name: "<subheading_name>", child: [{name: "<subheading_name>", child: [...]}, ...]}, ...]}]}. Give me only json and nothing else. Create as many subheadings as necessary for an undergraduate student.
      `;

    const structuredData = await generateFromLLM(topicPrompt);
    console.log("Raw structured data:", structuredData);

    // Parse structured data from LLM response
    let structuredResponse;
    try {
      // Extract the JSON string from the response
      const jsonStart = structuredData.indexOf("{");
      const jsonEnd = structuredData.lastIndexOf("}") + 1; // Include the closing brace
      const jsonString = structuredData.substring(jsonStart, jsonEnd).trim();
      console.log("JSON String to parse:", jsonString); // Log the substring before parsing

      // Validate JSON format before parsing
      if (jsonString.includes("\n") || jsonString.includes("\r")) {
        console.warn("JSON string contains control characters:", jsonString);
      }

      structuredResponse = JSON.parse(jsonString);
    } catch (err) {
      console.error("Error parsing structured JSON:", err);
      return res.status(400).send("Invalid JSON received from LLM");
    }

    // Step 2: Prepare the main topic for insertion into the database
    const mainTopic = structuredResponse; // Assuming the first element is the main topic
    const topicDocument = {
      id: new ObjectId(), // MongoDB will generate a unique ID
      name: mainTopic.name,
      content: "", // Content is not generated; set to empty
      child: mainTopic.child.map((child) => ({
        id: new ObjectId(), // Generate unique ID for each child
        name: child.name,
        content: "", // Content is not generated; set to empty
        child: child.child || [], // Include child subheadings if any
      })), // Directly assign child topics
    };
    console.log("Prepared topic document:", topicDocument);
    const topicId = await insertTopic(db, topicDocument);
    console.log("Inserted topic into database with ID:", topicId);

    // Step 3: Update the topic with generated children (if any)
    const isUpdated = await updateTopicWithChildren(
      db,
      topicId,
      topicDocument.child
    );

    if (isUpdated) {
      res.status(201).send(`Topic and subheadings added with _id: ${topicId}`);
    } else {
      res.status(500).send("Failed to update topic with subheadings");
    }
  } catch (error) {
    console.error("Error processing prompt:", error);
    res.status(500).send("Error generating topic or subheadings");
  }
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
