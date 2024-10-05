const { MongoClient, ObjectId } = require("mongodb");
const dotenv = require("dotenv");

dotenv.config();

const client = new MongoClient(process.env.MONGO_URI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Connect to MongoDB
async function connectToDB() {
  try {
    await client.connect();
    console.log("Connected to MongoDB");
    return client.db("mydatabase"); // Ensure "mydatabase" is your actual DB name
  } catch (err) {
    console.error("Failed to connect to MongoDB:", err);
    throw err;
  }
}

// Insert a topic into the database
async function insertTopic(db, topicData) {
  try {
    const result = await db.collection("topics").insertOne(topicData);
    console.log("Inserted topic with ID:", result.insertedId);
    return result.insertedId;
  } catch (err) {
    console.error("Error inserting topic:", err);
    throw err;
  }
}

// Update a topic by adding subtopics/children
async function updateTopicWithChildren(db, topicId, subtopics) {
  try {
    const result = await db
      .collection("topics")
      .updateOne(
        { _id: new ObjectId(topicId) },
        { $set: { child: subtopics } }
      );
    console.log("Updated topic:", result.modifiedCount > 0);
    return result.modifiedCount > 0;
  } catch (err) {
    console.error("Error updating topic:", err);
    throw err;
  }
}


module.exports = {
  connectToDB,
  insertTopic,
  updateTopicWithChildren,
  ObjectId,
};
