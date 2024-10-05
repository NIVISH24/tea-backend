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

// Update a child topic's content
async function updateTopicWithChildren(db, parentId, childId, content) {
  try {
    const result = await db
      .collection("topics")
      .updateOne(
        { "child._id": childId },
        { $set: { "child.$.content": content } }
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
  updateTopicWithChildren,
  ObjectId,
};
