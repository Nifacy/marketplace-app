import React, { useContext, useState } from "react";
import styles from "./styles.module.css";

import { Input } from "../../components/Input";
import { Button } from "../../components/Button";
import { Link, useNavigate } from "react-router-dom";
import { Navigation } from "../../App";

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
    try {
      setIsLoading(true);

      const userResponse = await fetch(`http://localhost:3000/client/${login}/${password}`).then((response) =>
        response.json()
      );
      // если запросы на получение клиента и продавца разные, используем конструкцию {isClient ? `...` : `...`}

      if (userResponse) {
        const path = isClient ? `/client/${userResponse.id}` : `/customer/${userResponse.id}`;
        if (isClient) {
          setClientId(userResponse.id);
        } else {
          setCustomerId(userResponse.id);
        }
        navigate(path);
      }
    } catch (error) {
      setIsError(true);
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
