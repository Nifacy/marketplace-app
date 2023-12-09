import React from "react";
import styles from "./styles.module.css";

import { Link } from "react-router-dom";

export const Nav = () => {
  return (
    <div className={styles.nav}>
      <Link to="/">
        <img style={{ width: "40px", height: "40px" }} src="../../img/home-2.jpg" alt="home" />
      </Link>
      <Link to="/">
        <img style={{ width: "40px", height: "40px" }} src="../../img/home-2.jpg" alt="user" />
      </Link>
      <Link to="/">
        <img style={{ width: "40px", height: "40px" }} src="../../img/home-2.jpg" alt="cart" />
      </Link>
      <Link to="/">
        <img style={{ width: "40px", height: "40px" }} src="../../img/home-2.jpg" alt="like" />
      </Link>
    </div>
  );
};
