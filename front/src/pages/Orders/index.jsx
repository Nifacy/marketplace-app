import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";

import { Nav } from "../../components/Nav";
import { OrderItem } from "../../components/OrderItem";

export const Orders = () => {
  const { customerId, clientId } = useContext(Navigation);

  const [items, setItems] = useState([
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      order: "qweqweqwe",
      description: "fhhfhfhfhfh", // !!!
      price: 123,
      // В ORDERITEM ПЕРЕДАЕТСЯ ID, важно!
    },
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      order: "qweqweqwe",
      description: "fhhfhfhfhfh", // !!!
      price: 123,
      // В ORDERITEM ПЕРЕДАЕТСЯ ID, важно!
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const items = await fetch(`http://localhost:3000/orders`).then((res) => res.json()); // заказы (ИСПОЛЬЗУЕМ customerId, clientId)
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
