const axios = require("axios");

async function generateFromLLM(prompt) {
  try {
    const response = await axios.post("http://localhost:11434/api/generate", {
      model: "llama3.2",
      prompt: prompt,
      stream: false, // Ensuring the stream is off
    });

    return response.data.response; // Return the generated response
  } catch (error) {
    console.error("Error calling LLM:", error);
    throw error;
  }
}

module.exports = { generateFromLLM };
