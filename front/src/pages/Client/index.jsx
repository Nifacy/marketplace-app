import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

import { Nav } from "../../components/Nav";
import { CardItem } from "../../components/CardItem";
import { Input } from "../../components/Input";

export const Client = () => {
  const [items, setItems] = useState([
    {
      url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      name: "qweqweqwe",
      price: 123,
      // В CARDITEM ПЕРЕДАЕТСЯ ID, важно!
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchValue, setSearchValue] = useState("");

  const handleOnChangeSearch = (event) => {
    setSearchValue(event.target.value);
  };

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

  const renderItems = () => {
    return (
      isLoading ? [...Array(8)] : items.filter((item) => item.name.toLowerCase().includes(searchValue.toLowerCase()))
    ).map((item, index) => {
      return <CardItem {...item} key={index} isLoading={isLoading} />;
    });
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <Input placeholder="Поиск" value={searchValue} onChange={handleOnChangeSearch} />
        <div className={styles.items}>{renderItems()}</div>
      </div>
    </div>
  );
};
