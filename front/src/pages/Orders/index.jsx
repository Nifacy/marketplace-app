import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

import { Nav } from "../../components/Nav";
import { OrderItem } from "../../components/OrderItem";

import { api } from "../../api";

export const Orders = () => {
  const [items, setItems] = useState([
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      order: "qweqweqwe",
      description: "fhhfhfhfhfh", // !!!
      price: 123,
    },
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      order: "qweqweqwe",
      description: "fhhfhfhfhfh", // !!!
      price: 123,
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        let items = [];

        for (const order of await api.getOrders()) {
          items.push({
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
            return <OrderItem {...item} key={index} isLoading={isLoading} />;
          })}
        </div>
      </div>
    </div>
  );
};
