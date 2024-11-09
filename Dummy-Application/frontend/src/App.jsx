import React from "react";
import ResearchComponent from "../src/components/ResearchComponent";  // Import the ResearchComponent
import styles from '../src/styles/research.module.css'

const App = () => {
  return (
    <div>
      <h1 className={styles.h1}>Research Document Generator</h1>
      <ResearchComponent />  {/* Use the ResearchComponent */}
    </div>
  );
};

export default App;
