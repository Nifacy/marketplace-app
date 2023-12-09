import React, { useState } from "react";
import styles from "./styles.module.css";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { useNavigate } from "react-router-dom";

export const ClientReg = () => {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");

  const [сountry, setСountry] = useState("");
  const [house, setHouse] = useState("");
  const [city, setCity] = useState("");
  const [apartment, setApartment] = useState("");
  const [street, setStreet] = useState("");
  const [building, setBuilding] = useState("");

  const handleOnChangeName = (event) => {
    setName(event.target.value);
  };
  const handleOnChangeSurname = (event) => {
    setSurname(event.target.value);
  };
  const handleOnChangePhone = (event) => {
    setPhone(event.target.value);
  };
  const handleOnChangeEmail = (event) => {
    setEmail(event.target.value);
  };
  const handleOnChangeCountry = (event) => {
    setСountry(event.target.value);
  };
  const handleOnChangeHouse = (event) => {
    setHouse(event.target.value);
  };
  const handleOnChangeCity = (event) => {
    setCity(event.target.value);
  };
  const handleOnChangeApartment = (event) => {
    setApartment(event.target.value);
  };
  const handleOnChangeStreet = (event) => {
    setStreet(event.target.value);
  };
  const handleOnChangeBuilding = (event) => {
    setBuilding(event.target.value);
  };
  const handleOnChangeLogin = (event) => {
    setLogin(event.target.value);
  };
  const handleOnChangePassword = (event) => {
    setPassword(event.target.value);
  };

  async function handleEnter() {
    try {
      setIsLoading(true);

      const data = {
        // ваш объект данных (ключ - значение)
      };

      const requestOptions = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      };

      const response = await fetch(`http://localhost:3000/client/registration`, requestOptions).then((response) =>
        response.json()
      );

      if (response) {
        navigate("/login");
      }
    } catch (error) {
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className={styles.main}>
      <h3>Welcome first</h3>
      <h4>Данные для входа:</h4>
      <div className={styles.personal}>
        <Input value={login} onChange={handleOnChangeLogin} placeholder="Логин" type="text" />
        <Input value={password} onChange={handleOnChangePassword} placeholder="Пароль" type="password" />
      </div>
      <h4>Личные данные:</h4>
      <div className={styles.personal}>
        <Input value={name} onChange={handleOnChangeName} placeholder="Имя" type="text" />
        <Input value={surname} onChange={handleOnChangeSurname} placeholder="Фамилия" type="text" />
        <Input value={phone} onChange={handleOnChangePhone} placeholder="Телефон" type="phone" />
        <Input value={email} onChange={handleOnChangeEmail} placeholder="Email" type="email" />
      </div>
      <h4>Адрес:</h4>
      <div className={styles.address}>
        <Input value={сountry} onChange={handleOnChangeCountry} placeholder="Страна" type="text" />
        <Input value={house} onChange={handleOnChangeHouse} placeholder="Дом" type="text" />
        <Input value={city} onChange={handleOnChangeCity} placeholder="Город" type="text" />
        <Input value={apartment} onChange={handleOnChangeApartment} placeholder="Квартира" type="text" />
        <Input value={street} onChange={handleOnChangeStreet} placeholder="Улица" type="text" />
        <Input value={building} onChange={handleOnChangeBuilding} placeholder="Строение" type="text" />
      </div>

      <Button size={250} onClick={handleEnter}>
        Зарегестрироваться
      </Button>
      <p style={{ color: "red", opacity: isError ? 1 : 0 }}>
        Некорректные данные в форме <br />
      </p>
      <p style={{ opacity: isLoading ? 1 : 0 }}>Загрузка</p>
    </div>
  );
};
