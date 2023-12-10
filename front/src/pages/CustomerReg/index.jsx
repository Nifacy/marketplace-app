import React, { useState } from "react";
import styles from "./styles.module.css";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { useNavigate } from "react-router-dom";

import * as api from "../../api"
import * as tokenManager from "../../tokenManager"

export const CustomerReg = () => {
  const navigate = useNavigate();

  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [errorDescription, setErrorDescription] = useState("");

  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [telegram, setTelegram] = useState("");
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
  const handleOnChangeEmail = (event) => {
    setEmail(event.target.value);
  };
  const handleOnChangePhone = (event) => {
    setPhone(event.target.value);
  };
  const handleOnChangeTelegram = (event) => {
    setTelegram(event.target.value);
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
  }
  const handleOnChangePassword = (event) => {
    setPassword(event.target.value);
  }

  async function handleEnter() {
    const registerData = {
      credentials: {
        login: login,
        password: password,
      },
      info: {
        name: name,
        contacts: {
          phone: phone,
          email: email,
          telegram: telegram,
        },
        address: {
          street: street,
          city: city,
          country: сountry,
          postal_code: "12345", 
          house: parseInt(house),
          entrance: parseInt(apartment),
          appartment: parseInt(building),
        },
      },
    };

    try {
      setIsLoading(true);
      const response = await api.auth.registerSupplier(registerData);
      tokenManager.saveToken("supplier", response.token);
      navigate("/login"); // TODO: move to home page when authorised
    } catch(error) {
      if (error instanceof api.exception.AlreadyExists) {
        setErrorDescription("Пользователь с данным логином уже существует");
        setIsError(true);
      } else if (error instanceof api.exception.RequestFailed) {
        setErrorDescription("Неверный формат данных");
        setIsError(true);
      } else {
        throw error;
      }
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
        <Input value={name} onChange={handleOnChangeName} placeholder="Название компании" type="text" />
        <Input value={email} onChange={handleOnChangeEmail} placeholder="Email" type="text" />
        <Input value={phone} onChange={handleOnChangePhone} placeholder="Номер телефона" type="text" />
        <Input value={telegram} onChange={handleOnChangeTelegram} placeholder="Telegram" type="text" />
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
       { errorDescription } <br />
      </p>
      <p style={{ opacity: isLoading ? 1 : 0 }}>Загрузка</p>
    </div>
  );
};
