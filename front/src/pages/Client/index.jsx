import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";

// import { useNavigate } from "react-router-dom";
import { Nav } from "../../components/Nav";
import { Search } from "../../components/Search";
import { CardItem } from "../../components/CardItem";

export const Client = () => {
  //   const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        setIsLoading(true);
        const items = await fetch(`http://localhost:3000/ALLitems`).then((res) => res.json());
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
    return (isLoading ? [...Array(8)] : items) //items.filter((item) => item.title.toLowerCase().includes(searchValue.toLowerCase()))
      .map((item, index) => {
        return (
          <CardItem
            {...item}
            key={index}
            // onClickPlus={(obj) => onAddToCart(obj)}
            // onClickFavorite={(obj) => onAddToFavorite(obj)}
            isLoading={isLoading}
          />
        );
      });
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <Search />
        <div className={styles.items}>{renderItems()}</div>
      </div>
    </div>
  );
};
