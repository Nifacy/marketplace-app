import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";

import { Nav } from "../../components/Nav";
import { OrderItem } from "../../components/OrderItem";

import { api } from "../../api";

export const Orders = () => {
  const { customerId, clientId } = useContext(Navigation);

  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        let items = [];

        for (const order of await api.getOrders()) {
          items.push({
            id: order.id,
            url: order.product.info.images[0],
            order: `Заказ №${order.id}`,
            description: `Доставка продавцом ${order.product.supplier.info.name}`,
            price: order.price,
          });
        }

        setItems(items);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <div className={styles.items}>
          {items.map((item, index) => {
            return <OrderItem {...item} isLoading={isLoading} />;
          })}
        </div>
      </div>
    </div>
  );
};
