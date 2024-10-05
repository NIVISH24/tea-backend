import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown'; // Import the react-markdown library


const ChildTopics = ({ childTopics, parentId, handleContentGeneration }) => {
  return (
    <div className="ml-4 bg-gradient-to-r from-blue-300 to-blue-500 rounded-lg p-2">
      {childTopics.map((child) => (
        <div key={child._id} className="text-lg text-white border">
          <div
            onClick={() => handleContentGeneration(parentId, child._id)}
            className="cursor-pointer"
          >
            {child.name}
          </div>
          {/* Recursive call for further child topics */}
          {child.child && child.child.length > 0 && (
            <ChildTopics
              childTopics={child.child}
              parentId={child._id}
              handleContentGeneration={handleContentGeneration}
            />
          )}
        </div>
      ))}
    </div>
  );
};


const Topics = () => {
  const [topics, setTopics] = useState([]);
  const [expandedTopic, setExpandedTopic] = useState(null);
  const [selectedContent, setSelectedContent] = useState('');

  // Fetch topics from the API
  useEffect(() => {
    const fetchTopics = async () => {
      try {
        const response = await fetch('http://localhost:3000/getTopics');
        const data = await response.json();
        setTopics(data);
      } catch (error) {
        console.error('Error fetching topics:', error);
      }
    };
    fetchTopics();
  }, []);

  // Toggle the expanded state of the topic
  const toggleExpand = (id) => {
    setExpandedTopic(expandedTopic === id ? null : id);
  };

  // Function to handle content generation
  const handleContentGeneration = async (parentId, childId) => {
    try {
      const response = await fetch('http://localhost:3000/generateContentForChild', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ parentId, childId }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setSelectedContent(data.content);
    } catch (error) {
      console.error('Error generating content:', error);
      alert('Failed to generate content. Please try again.');
    }
  };

  return (
    <>
      <div className=" p-4 w-3/7">
        <div className="space-y-4">
          {topics.map((topic) => (
            <div key={topic._id}>
              <div
                onClick={() => toggleExpand(topic._id)}
                className="cursor-pointer bg-gradient-to-r from-blue-700 to-cyan-800 border rounded-xl p-2 text-lg text-white"
              >
                {topic.name}
              </div>
              {expandedTopic === topic._id && topic.child && topic.child.length > 0 && (
                <ChildTopics
                  childTopics={topic.child}
                  parentId={topic._id}
                  handleContentGeneration={handleContentGeneration}
                />
              )}
            </div>
          ))}
        </div>
      </div>
      <div className="rounded-3xl h-full w-4/7 w-full p-4 m-4 border h-[calc(100% - 10vh)] bg-blue-950">
        {selectedContent ? (
          <ReactMarkdown className="text-lg text-blue-100">{selectedContent}</ReactMarkdown>
        ) : (
          <div className="text-gray-400">Select a topic to see the content.</div>
        )}
      </div>
    </>
  );
};

export default Topics;