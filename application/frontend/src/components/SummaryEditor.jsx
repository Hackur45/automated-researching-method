import React, { useEffect, useState } from 'react';
import { CKEditor } from '@ckeditor/ckeditor5-react';
import ClassicEditor from '@ckeditor/ckeditor5-build-classic';
import marked from 'marked';

function ResearchEditor({ generatedContent, setGeneratedContent }) {
  const [editorContent, setEditorContent] = useState('');

  useEffect(() => {
    // Convert the initial markdown (if available) to HTML
    if (generatedContent) {
      setEditorContent(marked(generatedContent));
    }
  }, [generatedContent]);

  const handleEditorChange = (event, editor) => {
    const data = editor.getData();
    // Convert the HTML back to markdown
    const newContent = marked.parse(data);
    setGeneratedContent(newContent);  // Update the parent state
  };

  return (
    <div>
      <h2>Edit Research Paper</h2>
      <CKEditor
        editor={ClassicEditor}
        data={editorContent}
        onChange={handleEditorChange}
        config={{
          toolbar: [
            'heading', 'bold', 'italic', 'underline', '|', 'link', 'bulletedList', 'numberedList', '|', 'blockquote'
          ]
        }}
      />
    </div>
  );
}

export default ResearchEditor;
