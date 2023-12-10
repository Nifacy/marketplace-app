import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";

import { Nav } from "../../components/Nav";
import { Button } from "../../components/Button";
import { useNavigate } from "react-router-dom";

export const FullCardItem = () => {
  const { isClient, clientId, customerId, itemId } = useContext(Navigation);
  const navigate = useNavigate();
  const [fav, setFav] = useState(false);

  const [item, setItem] = useState({
    url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
    name: "qweqweqwe",
    description: "asdasdasdads",
    customer: "blalbalba",
    price: 123,
  });
  // const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      try {
        const resp = await fetch(`http://localhost:3000/item/:id/favorite`).then((res) => res.json()); // запрос избранного
        setFav(resp);
      } catch (error) {
        console.log(error);
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchData() {
      try {
        // setIsLoading(true);
        const item = await fetch(`http://localhost:3000/item/:id`).then((res) => res.json()); // товар
        setItem(item);
      } catch (error) {
        console.log(error);
      } finally {
        // setIsLoading(false);
      }
    }
    fetchData();
  }, []);

  async function handleOnChnageFavorite() {
    try {
      if (fav) {
        // запрос на удаление из избранного
      } else {
        // запрос на добавление в избранное
      }
      setFav(!fav);
    } catch (error) {
      console.log(error);
    }
  }

  const handleOnClickBuy = async () => {
    try {
      // setIsLoading(true);
      const data = {
        // ваш объект данных (ключ - значение)
      };

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };

      const buyResponse = await fetch(`http://localhost:3000/orders/add`, requestOptions).then((response) =>
        response.json()
      ); // добавление заказа

      if (buyResponse) {
        const path = isClient ? `/client/${clientId}/orders` : `/customer/${customerId}/orders`;
        navigate(path);
      }
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  };

  const handleOnClickUpdate = () => {
    const pathUpd = `/customer/${customerId}/item/${itemId}/edit`;
    navigate(pathUpd);
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <div className={styles.item}>
          <div>
            <img src={item.url} alt="1" />
          </div>
          <div className={styles.infoBut}>
            <div className={styles.info}>
              <h3>{item.name}</h3>
              <h5 style={{ color: "gray" }}>{item.description}</h5>
              <h5 style={{ color: "gray" }}>{item.customer}</h5>
              <h4>{item.price} $</h4>
            </div>
            <div className={styles.buttons}>
              {isClient && (
                <Button onChange={handleOnClickBuy} size="250">
                  Купить
                </Button>
              )}
              {isClient && (
                <Button onChange={handleOnChnageFavorite} color="gray" size="250">
                  {fav ? "Убрать из" : "Добавить в"} wishlist
                </Button>
              )}
              {!isClient && (
                <Button onChange={handleOnClickUpdate} size="250">
                  Редактировать
                </Button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
