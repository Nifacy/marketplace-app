import React from "react";
import styles from "./styles.module.css";

export const Input = (props) => {
  const { value, onChange, placeholder, type } = props;
  return <input type={type} placeholder={placeholder} className={styles.input} value={value} onChange={onChange} />;
};
