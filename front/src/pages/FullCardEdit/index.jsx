import React, { useContext, useEffect, useState } from "react";
import styles from "./styles.module.css";
import { Navigation } from "../../App";

import { Nav } from "../../components/Nav";
import { Button } from "../../components/Button";
import { useNavigate } from "react-router-dom";
import { Input } from "../../components/Input";
import { Modal } from "../../components/Modal";

export const FullCardEdit = () => {
  const { customerId, itemId } = useContext(Navigation);
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [price, setPrice] = useState();

  const [showModalAddImg, setShowModalAddImg] = useState(false);

  const [item, setItem] = useState({
    urls: [
      "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
      "https://gas-kvas.com/uploads/posts/2023-02/1675489758_gas-kvas-com-p-izobrazheniya-i-kartinki-na-fonovii-risuno-41.jpg",
    ],
    name: "qweqweqwe",
    description: "asdasdasdads",
    customer: "blalbalba",
    price: 123,
  });
  // const [isLoading, setIsLoading] = useState(false);

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

  const handleOnClickUpdate = async () => {
    try {
      // setIsLoading(true);
      const data = {
        // ваш объект данных (ключ - значение)
        // name, description, price
      };

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };

      const updateResponse = await fetch(`http://localhost:3000/item/:id/update`, requestOptions).then((response) =>
        response.json()
      ); // сохранение новых данных заказа

      if (updateResponse) {
        const pathUpd = `/customer/${customerId}/item/${itemId}`;
        navigate(pathUpd);
      }
    } catch (error) {
      console.log(error);
    } finally {
      // setIsLoading(false);
    }
  };

  const handleOnChangeName = (event) => {
    setName(event.target.value);
  };
  const handleOnChangeDescription = (event) => {
    setDescription(event.target.value);
  };
  const handleOnChangePrice = (event) => {
    setPrice(event.target.value);
  };

  const handleSubmitUrl = async (event) => {
    event.preventDefault();
    try {
      // setIsLoading(true);
      const data = {
        // ваш объект данных (ключ - значение)
        // url
      };

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };

      await fetch(`http://localhost:3000/item/add/image`, requestOptions).then((response) => response.json()); // добавление картинки
    } catch (error) {
      console.log(error);
    } finally {
      setShowModalAddImg(false);
    }
  };

  return (
    <div className={styles.container}>
      <Nav />
      <div className={styles.main}>
        <div className={styles.item}>
          <div className={styles.images}>
            {item.urls.map((url, index) => (
              <img key={index} src={url} alt="1" />
            ))}
            {item.urls.length <= 3 && (
              <button onClick={() => setShowModalAddImg(true)} className={styles.addImg}>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50" width="100px" height="100px">
                  <path d="M 25 2 C 12.309295 2 2 12.309295 2 25 C 2 37.690705 12.309295 48 25 48 C 37.690705 48 48 37.690705 48 25 C 48 12.309295 37.690705 2 25 2 z M 25 4 C 36.609824 4 46 13.390176 46 25 C 46 36.609824 36.609824 46 25 46 C 13.390176 46 4 36.609824 4 25 C 4 13.390176 13.390176 4 25 4 z M 24 13 L 24 24 L 13 24 L 13 26 L 24 26 L 24 37 L 26 37 L 26 26 L 37 26 L 37 24 L 26 24 L 26 13 L 24 13 z" />
                </svg>
              </button>
            )}
          </div>
          <div className={styles.infoBut}>
            <div className={styles.info}>
              <Input value={name} onChange={handleOnChangeName} placeholder="Название товара" />
              <Input value={description} onChange={handleOnChangeDescription} placeholder="Описание товара" />
              <Input value={price} onChange={handleOnChangePrice} placeholder="2999 $" />
            </div>
            <div className={styles.buttons}>
              <Button onChange={handleOnClickUpdate} size="250">
                Сохранить
              </Button>
            </div>
          </div>
        </div>
      </div>
      <Modal active={showModalAddImg} setActive={setShowModalAddImg}>
        <form
          style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "50px" }}
          onSubmit={handleSubmitUrl}
        >
          <Input placeholder="Url" />
          <Button size="250">Добавить картинку</Button>
        </form>
      </Modal>
    </div>
  );
};
