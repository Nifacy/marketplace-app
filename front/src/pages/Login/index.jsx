import React, { useContext, useState } from "react";
import styles from "./styles.module.css";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Link, useNavigate } from "react-router-dom";
import { Navigation } from "../../App";

import * as tokenManager from "../../tokenManager";
import * as api from "../../api";

export const Login = () => {
  const { isClient, setClientId, setCustomerId } = useContext(Navigation);
  const navigate = useNavigate();

  const [login, setLogin] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleOnChangeLogin = (event) => {
    setLogin(event.target.value);
  };

  const handleOnChangePassword = (event) => {
    setPassword(event.target.value);
  };

  async function handleEnter() {
    setIsLoading(true);

    const credentials = {
      login: login,
      password: password,
    };

    try {
      setIsLoading(true);
      const response = await api.auth.authCustomer(credentials);
      tokenManager.saveToken(isClient ? "customer" : "supplier", response.token);
      navigate("/login"); // TODO: move to home page when authorised
    } catch(error) {
      if (error instanceof api.exception.InvalidCredentials) {
        setIsError(true);
      } else if (error instanceof api.exception.RequestFailed) {
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
      <h3>Welcome back</h3>
      <Input value={login} onChange={handleOnChangeLogin} placeholder="Login" type="text" />
      <Input value={password} onChange={handleOnChangePassword} placeholder="Password" type="password" />
      <p>
        Нет аккаунта?{" "}
        <Link to={isClient ? "/client/registration" : "/customer/registration"}>
          <span>Зарегестрироваться</span>
        </Link>
      </p>
      <Button onClick={handleEnter}>Войти</Button>
      <p style={{ color: "red", opacity: isError ? 1 : 0 }}>
        Неправильное имя или пароль <br />
      </p>
      <p style={{ opacity: isLoading ? 1 : 0 }}>Загрузка</p>
    </div>
  );
};
