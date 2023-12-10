import React, { useContext } from "react";
import styles from "./styles.module.css";
import { Link } from "react-router-dom";
import { Navigation } from "../../App";

export const OrderItem = (props) => {
  const { isClient, clientId, customerId, orderId, setOrderId } = useContext(Navigation);

  const { id, order, price, description, url } = props;

  setOrderId(id);
  const itemPath = isClient ? `/client/${clientId}/order/${orderId}` : `/customer/${customerId}/order/${orderId}`;

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
