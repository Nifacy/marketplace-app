import React, { useEffect, useState } from "react";
import styles from "./styles.module.css";
import { useParams } from 'react-router-dom';

import { Nav } from "../../components/Nav";
import { Button } from "../../components/Button";

import { api, tokenManager } from "../../api";

export const FullOrderItem = () => {
  const { itemId } = useParams();

  const isClient = tokenManager.getToken().type === "customer";
  const userId = tokenManager.getToken().id;
  const orderId = parseInt(itemId);

  const [isDisable, setIsDisable] = useState(false);

  const [item, setItem] = useState({
    url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
    name: "Heroin",
    price: 123,
    description: "asdasdasdads",
    address: "1231",
    productInfo: [],
    status: "офигеть",
    order: "#12121111",
  });

  // const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      // setIsLoading(true);
      const order = await api.getOrder(orderId);

      const creationDate = new Date(order.creation_datetime);
      let productInfo = [
        ["Получатель", `${order.customer.info.first_name} ${order.customer.info.last_name}`],
        ["Адрес", `${order.target_address.city}, ${order.target_address.street}, д. ${order.target_address.house}, кв. ${order.target_address.appartment}`],
        ["Дата заказа", `${creationDate.getDay()}.${creationDate.getMonth()}.${creationDate.getFullYear()}`],
      ];
      const item = {
        url: order.product.info.images[0],
        name: order.product.info.product_name,
        price: order.product.info.price,
        description: "Какое-то описание", // TODO: добавить мапу статусов
        address: order.target_address,
        productInfo: productInfo,
        status: order.status,
        order: `Заказ №${order.id}`,
      };
      setItem(item);
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  }

  useEffect(() => {
    const interval = setInterval(fetchData, 1_000); // Call fetchData every 10 seconds
    return () => {
      clearInterval(interval); // Clean up the interval when the component unmounts
    };
  }, []);

  const handleOnClickConfirm = async () => {
    try {
      // setIsLoading(true);
      setIsDisable(true);
      const data = {
        // ваш объект данных (ключ - значение)
      };

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };

      await fetch(`http://localhost:3000/orders/add`, requestOptions).then((response) => response.json()); // подтверждение заказа
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <div className={styles.item}>
          <div className={styles.info}>
            <h5 style={{ fontSize: "36px", fontWeight: "bold" }}>{item.order}</h5>
            {
              item.productInfo.map((record) => {
                return <h5 style={{ fontSize: "24px", color: "gray" }}>{record[0]}: {record[1]}</h5>;
              })
            }
            <h3>{item.name}</h3>
            <img src={item.url} alt="1" />
            <h4 style={{ fontSize: "24px", fontWeight: "bold" }}>Цена: {item.price} $</h4>
          </div>
          <div className={styles.infoBut}>
            <p style={{ fontSize: "36px", fontWeight: "bold" }}>Cтатус: {item.status}</p>
            <h5 style={{ fontSize: "20px", color: "gray" }}>{item.description}</h5>

            <Button isDisable={isDisable} onChange={handleOnClickConfirm} size="340">
              Подтвердить
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};
