const axios = require("axios");

async function generateFromLLM(prompt) {
  try {
    const response = await axios.post(
      "http://localhost:11434/api/generate",
      {
        model: "llama3.2",
        prompt: prompt,
      },
      {
        responseType: "stream", // Handle streaming response
      }
    );

    let result = "";

    return new Promise((resolve, reject) => {
      response.data.on("data", (chunk) => {
        const chunkString = chunk.toString();

        const json = JSON.parse(chunkString);
        result += json.response;
      });

      response.data.on("end", () => {
        console.log("Final accumulated result:", result);
        try {
          resolve(result); // Return the raw result for further processing
        } catch (err) {
          console.error("Error processing streamed response:", err);
          reject(err);
        }
      });

      response.data.on("error", (err) => {
        console.error("Stream error:", err);
        reject(err);
      });
    });
  } catch (error) {
    console.error("Error calling LLM:", error);
    throw error;
  }
}

module.exports = { generateFromLLM };
