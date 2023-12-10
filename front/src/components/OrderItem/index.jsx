import React from "react";
import styles from "./styles.module.css";

export const OrderItem = (props) => {
  const { order, price, description, url } = props;

  return (
    <div className={styles.card}>
      <div className={styles.info}>
        <h3>{order}</h3>
        <h4 style={{ color: "gray" }}>{description}</h4>
        <h5>{price} $</h5>
      </div>
      <div>
        <img alt="1" src={url} />
      </div>
    </div>
  );
};
