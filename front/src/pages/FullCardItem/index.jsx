import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";
import { useParams } from 'react-router-dom';

import { Nav } from "../../components/Nav";
import { Button } from "../../components/Button";
import { useNavigate } from "react-router-dom";

import { api, tokenManager } from "../../api";

export const FullCardItem = () => {
  const navigate = useNavigate();
  const { itemId } = useParams();
  const isClient = tokenManager.getToken().type === "customer";
  const userId = tokenManager.getToken().id;
  const [fav, setFav] = useState(false);

  const productId = parseInt(itemId);

  const [item, setItem] = useState({
    url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
    name: "Loading...",
    description: "",
    customer: "",
    price: 0,
  });

  // const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchData() {
      console.log("fetch data...");
      try {
        const favoriteIds = (await api.getFavorites()).map((product) => product.id);
        setFav(favoriteIds.includes(productId));
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
        const product = await api.getProduct(productId);
        const item = {
          url: product.info.images[0],
          name: product.info.product_name,
          description: product.info.description,
          customer: product.supplier.info.name,
          price: product.info.price,
        };
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
        await api.removeFromFavorites(productId);
      } else {
        await api.addToFavorites(productId);
      }
      setFav(!fav);
    } catch (error) {
      console.log(error);
    }
  }

  const handleOnClickBuy = async () => {
    try {
      // setIsLoading(true);
      await api.createOrder(productId);

      const path = isClient ? `/client/${userId}/orders` : `/customer/${userId}/orders`;
      navigate(path);
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  };

  const handleOnClickUpdate = () => {
    const pathUpd = `/customer/${userId}/item/${itemId}/edit`;
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
                <Button onClick={handleOnClickBuy} size="250">
                  Купить
                </Button>
              )}
              {isClient && (
                <Button onClick={handleOnChnageFavorite} color="gray" size="250">
                  {fav ? "Убрать из" : "Добавить в"} wishlist
                </Button>
              )}
              {!isClient && (
                <Button onClick={handleOnClickUpdate} size="250">
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
