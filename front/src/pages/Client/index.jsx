import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

import { Nav } from "../../components/Nav";
import { CardItem } from "../../components/CardItem";
import { Input } from "../../components/Input";

import * as api from "../../api"

export const Client = () => {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [searchValue, setSearchValue] = useState("");

  const handleOnChangeSearch = (event) => {
    setSearchValue(event.target.value);
  };

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        await new Promise(resolve => setTimeout(resolve, 1000));
        let _items = [];

        for (const product of await api.api.getProducts()) {
          _items.push({
            productId: product.id,
            url: product.info.images[0],
            name: product.info.product_name,
            price: product.info.price,
            initialFav: product.in_favorites,
          });
        }
        setItems(_items);
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
      isLoading ? [...Array(8)] : items
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
