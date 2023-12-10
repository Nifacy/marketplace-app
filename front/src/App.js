import React, { createContext, useState } from "react";
import { Route, Routes } from "react-router-dom";
import "./App.css";

import { GetStarted } from "./pages/GetStarted";
import { Login } from "./pages/Login";
import { ClientReg } from "./pages/ClientReg";
import { CustomerReg } from "./pages/CustomerReg";
import { Client } from "./pages/Client/index";
import { ClientFav } from "./pages/ClientFav";
import { Orders } from "./pages/Orders";
import { FullCardItem } from "./pages/FullCardItem";

export const Navigation = createContext(null);

function App() {
  const [isClient, setIsClient] = useState(true);
  const [clientId, setClientId] = useState();
  const [customerId, setCustomerId] = useState();
  const [itemId, setItemId] = useState();

  return (
    <Navigation.Provider
      value={{
        isClient,
        setIsClient,
        clientId,
        setClientId,
        customerId,
        setCustomerId,
        itemId,
        setItemId,
      }}
    >
      <Routes>
        <Route>
          <Route path="/" element={<GetStarted />} />
          <Route path="/login" element={<Login />} />
          <Route path="/client/registration" element={<ClientReg />} />
          <Route path="/customer/registration" element={<CustomerReg />} />
          <Route path="/client/:id" element={<Client />} />
          <Route path="/client/:id/favorited" element={<ClientFav />} />
          <Route path="/client/:id/orders" element={<Orders />} />
          <Route path="/client/:id/item/:id" element={<FullCardItem />} />
          <Route path="/customer/:id/item/:id/edit" element={<FullCardItem />} />
          {/* проверить можно ли два id */}
          {/* <Route path="*" element={<NotFound />} /> */}
        </Route>
      </Routes>
    </Navigation.Provider>
  );
}

export default App;
