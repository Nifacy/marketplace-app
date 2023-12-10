import React, { useContext } from "react";
import styles from "./styles.module.css";
import { Link } from "react-router-dom";
import { useParams } from "react-router-dom";

import { api, tokenManager } from "../../api";

export const OrderItem = (props) => {
  const { id, order, price, description, url } = props;
  const isClient = tokenManager.getToken().type === "customer";
  const userId = tokenManager.getToken().id;

  const itemPath = isClient ? `/client/${userId}/order/${id}` : `/customer/${userId}/order/${id}`;

  return (
    <div className={styles.card}>
      <div className={styles.info}>
        <h3>{order}</h3>
        <h4 style={{ color: "gray" }}>{description}</h4>
        <h5>{price} $</h5>
      </div>
      <div>
        <Link to={itemPath}>
          <img alt="1" src={url} />
        </Link>
      </div>
    </div>
  );
};
