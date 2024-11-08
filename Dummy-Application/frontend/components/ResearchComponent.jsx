import React, { useState } from 'react';
import axios from 'axios';

const ResearchComponent = () => {
    const [query, setQuery] = useState("");
    const [loading, setLoading] = useState(false);

    const handleSearch = async () => {
        setLoading(true);
        try {
            const response = await axios.post(
                'http://127.0.0.1:5000/api/research',
                { query },
                { responseType: 'blob' } // Important for file download
            );

            // Create a URL for the document
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', 'Research_Document.docx'); // File name
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } catch (error) {
            console.error("Error fetching research document", error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Research Document Generator</h2>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter search query"
            />
            <button onClick={handleSearch} disabled={loading || !query}>
                {loading ? 'Generating...' : 'Generate Research Document'}
            </button>
        </div>
    );
};

export default ResearchComponent;
