import React from "react";
import styles from "./styles.module.css";

export const Button = (props) => {
  const { children, onClick, size, color } = props;

  return (
    <button style={{ width: `${size}px`, backgroundColor: `${color}` }} className={styles.button} onClick={onClick}>
      {children}
    </button>
  );
};
