import React from 'react';
import axios from 'axios';

function ExportButtons({ content }) {
  const handleExport = async (format) => {
    try {
      const response = await axios.post(`http://localhost:5000/api/export`, { content, format }, { responseType: 'blob' });
      const blob = new Blob([response.data]);
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `Research_Document.${format}`;
      link.click();
    } catch (error) {
      console.error('Error exporting document:', error);
      alert('There was an error exporting the document.');
    }
  };

  return (
    <div className="export-buttons">
      <button onClick={() => handleExport('docx')}>Export as Word</button>
      <button onClick={() => handleExport('pdf')}>Export as PDF</button>
    </div>
  );
}

export default ExportButtons;
