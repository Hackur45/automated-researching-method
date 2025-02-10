import React, { useState } from 'react';

function ResearchForm({ onSubmit, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      onSubmit(query);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter research topic"
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Generating...' : 'Generate Research'}
      </button>
    </form>
  );
}

export default ResearchForm;
