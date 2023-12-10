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
import { FullCardEdit } from "./pages/FullCardEdit";
import { Customer } from "./pages/Customer";
import { FullOrderItem } from "./pages/FullOrderItem";

export const Navigation = createContext(null);

function App() {
  const [isClient, setIsClient] = useState(false);
  const [clientId, setClientId] = useState();
  const [customerId, setCustomerId] = useState();
  const [itemId, setItemId] = useState();
  const [orderId, setOrderId] = useState();

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
        orderId,
        setOrderId,
      }}
    >
      <Routes>
        <Route>
          <Route path="/" element={<GetStarted />} />
          <Route path="/login" element={<Login />} />
          <Route path="/client/registration" element={<ClientReg />} />
          <Route path="/customer/registration" element={<CustomerReg />} />
          <Route path="/client/:clientId" element={<Client />} />
          <Route path="/customer/:customerId" element={<Customer />} />
          <Route path="/client/:clientId/favorited" element={<ClientFav />} />
          <Route path="/client/:clientId/orders" element={<Orders />} />
          <Route path="/customer/:customerId/orders" element={<Orders />} />
          <Route path="/client/:clientId/item/:itemId" element={<FullCardItem />} />
          <Route path="/customer/:customerId/item/:itemId" element={<FullCardItem />} />
          <Route path="/client/:clientId/order/:itemId" element={<FullOrderItem />} />
          <Route path="/customer/:customerId/order/:orderId" element={<FullOrderItem />} />
          <Route path="/customer/:customerId/item/:itemId/edit" element={<FullCardEdit />} />
          {/* проверить можно ли два id */}
          {/* <Route path="*" element={<NotFound />} /> */}
        </Route>
      </Routes>
    </Navigation.Provider>
  );
}

export default App;
