import React from "react";
import { Input } from "../Input";

export const Search = (props) => {
  const { placeholder } = props;
  //   const [searchName, setSearchName] = useState("");
  return <Input placeholder={placeholder} />;
};
