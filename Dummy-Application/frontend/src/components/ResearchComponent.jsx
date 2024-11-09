import React, { useState } from "react";
import axios from "axios";
import { CKEditor } from "@ckeditor/ckeditor5-react";
import ClassicEditor from "@ckeditor/ckeditor5-build-classic";
import styles from '../styles/research.module.css';

const ResearchComponent = () => {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);
    const [researchContent, setResearchContent] = useState("");

    const handleSearchSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await axios.post("http://localhost:5000/api/research", { query });

            // Log the response to inspect the structure
            console.log('Response data:', response.data);

            // Assuming the response contains research data and AI research paper content
            if (response.data.research_data) {
                let content = "";
                response.data.research_data.forEach(item => {
                    content += `<h2><a href="${item.url}" target="_blank">${item.url}</a></h2>`;
                    item.paragraphs.forEach(para => {
                        content += `<p>${para}</p>`;
                    });
                });

                // Include the AI-generated research paper if available
                if (response.data.ai_research_paper) {
                    content += `<h3>AI Generated Research Paper:</h3><p>${response.data.ai_research_paper}</p>`;
                }

                setResearchContent(content);
            } else {
                console.error("Unexpected response format:", response.data);
                setResearchContent("No research content found.");
            }
        } catch (error) {
            console.error("Error fetching research:", error);
            setResearchContent("Error fetching research, please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Research Document Generator</h2>

            <div className={styles.formContainer}>
                <form onSubmit={handleSearchSubmit}>
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Enter research topic"
                        className={styles.input}
                    />
                    <button type="submit" disabled={loading} className={styles.button}>
                        {loading ? "Loading..." : "Search"}
                    </button>
                </form>
            </div>

            <div className={styles.editorContainer}>
                {loading && <p className={styles.loadingText}>Loading research content...</p>}

                <CKEditor
                    editor={ClassicEditor}
                    data={researchContent} // Set the research content as data for CKEditor
                    onReady={(editor) => {
                        // You can add editor customization here if needed
                        console.log("Editor is ready!", editor);
                    }}
                />
            </div>
        </div>
    );
};

export default ResearchComponent;
