import React, { useContext } from "react";
import styles from "./styles.module.css";
import { Button } from "../../components/Button";
import { Link } from "react-router-dom";
import { Navigation } from "../../App";

export const GetStarted = () => {
  const { setIsClient } = useContext(Navigation);

  return (
    <div className={styles.main}>
      <div>
        <h3>Самые быстрые спиды и эйфоричные марки</h3>
      </div>
      <div className={styles.getStarted}>
        <h3>Get started</h3>
        <div className={styles.getStartedButtons}>
          <Link to="/login">
            <Button onClick={() => setIsClient(true)}>Покупатель</Button>
          </Link>
          <Link to="/login">
            {" "}
            <Button onClick={() => setIsClient(false)}>Продавец</Button>
          </Link>
        </div>
      </div>
    </div>
  );
};
