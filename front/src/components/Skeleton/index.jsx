import React from "react";
import ContentLoader from "react-content-loader";

export const Skeleton = (props) => (
  <div style={{ border: "1px solid gray" }}>
    <ContentLoader
      speed={2}
      width={170}
      height={220}
      viewBox="0 0 170 220"
      backgroundColor="#f3f3f3"
      foregroundColor="#ecebeb"
      {...props}
    >
      <rect x="20" y="18" rx="0" ry="0" width="130" height="130" />
      <rect x="20" y="160" rx="0" ry="0" width="73" height="17" />
      <rect x="20" y="180" rx="0" ry="0" width="54" height="17" />
    </ContentLoader>
  </div>
);
