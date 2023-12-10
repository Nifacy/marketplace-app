import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";

import { Nav } from "../../components/Nav";
import { Button } from "../../components/Button";
// import { useNavigate } from "react-router-dom";

export const FullOrderItem = () => {
  const { isClient, clientId, customerId, orderId } = useContext(Navigation);
  // const navigate = useNavigate();

  const [isDisable, setIsDisable] = useState(false);

  const [item, setItem] = useState({
    url: "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
    name: "Heroin",
    price: 123,
    description: "asdasdasdads",
    address: "1231",
    date: "12/12/12",
    status: "офигеть",
    order: "#12121111",
  }); // ВОЗМОЖНО БУДУТ НУЖНЫ ДОП ПОЛЯ, ДОБАВИТЬ ПО НЕОБХОДИМОСТИ . Изменить размер шрифта можно через fontSize

  // const [isLoading, setIsLoading] = useState(false);

  async function fetchData() {
    try {
      // setIsLoading(true);
      const item = await fetch(`http://localhost:3000/order/:id`).then((res) => res.json()); // заказ (clientId, customerId, orderId)
      setItem(item);
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  }

  // обсудить правильное решение при подключении бэкенда

  useEffect(() => {
    const interval = setInterval(fetchData, 10000); // Call fetchData every 10 seconds
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
            <h5 style={{ fontSize: "24px", color: "gray" }}>{item.address}</h5>
            {isClient && <h5 style={{ fontSize: "24px", color: "gray" }}>{item.date}</h5>}
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
