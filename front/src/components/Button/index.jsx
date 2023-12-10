import React from "react";
import styles from "./styles.module.css";

export const Button = (props) => {
  const { children, onClick, size, color, isDisable = false } = props;

  return (
    <button
      disable={isDisable.toString()}
      className={styles.button}
      style={{ width: `${size}px`, backgroundColor: `${color}` }}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
