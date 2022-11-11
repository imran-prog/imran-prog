/* eslint-disable @next/next/no-head-element */
import "../styles/globals.css";
import { Inter } from "@next/font/google";

// FONT
const inter = Inter();

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={inter.className}>
      <head>
        <title>Imran Akbar</title>
        <meta httpEquiv="X-UA-Compatible" content="IE=7" />
        <meta httpEquiv="X-UA-Compatible" content="ie=edge" />
        <meta httpEquiv="Content-Type" content="text/html;charset=UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta
          name="description"
          content="Are you getting bored out there come wisit this site to get more bore"
        />
        <meta name="keywords" content="Imran, Akbar, porfolio" />
      </head>
      <body>
        <div className="container">{children}</div>
      </body>
    </html>
  );
}
