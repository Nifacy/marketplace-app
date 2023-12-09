import React from "react";
import styles from "./styles.module.css";

export const Button = (props) => {
  const { children, onClick, size } = props;

  return (
    <button style={{ width: `${size}px` }} className={styles.button} onClick={onClick}>
      {children}
    </button>
  );
};
