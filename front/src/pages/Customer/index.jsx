import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

import { Nav } from "../../components/Nav";
import { CardItem } from "../../components/CardItem";

export const Customer = () => {
  const [items, setItems] = useState([
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      name: "qweqweqwe",
      price: 123,
      // В CARDITEM ПЕРЕДАЕТСЯ ID, важно!
    },
  ]);
  const [customerInfo, setCustomerInfo] = useState({
    companyName: "Ба Бу Бэ",
  });

  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const items = await fetch(`http://localhost:3000/ALLitems`).then((res) => res.json()); // id, name, price
        setItems(items);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const customerInfo = await fetch(`http://localhost:3000/customer/:id`).then((res) => res.json()); // информация о продаце (компания и т д)
        setCustomerInfo(customerInfo);
      } catch (error) {
        console.log(error);
      } finally {
        setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  const renderItems = () => {
    return (isLoading ? [...Array(8)] : items).map((item, index) => {
      return <CardItem {...item} key={index} isLoading={isLoading} />;
    });
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <h1>{customerInfo.companyName}</h1>
        <div className={styles.items}>{renderItems()}</div>
      </div>
    </div>
  );
};
