/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  experimental: {
    fontLoaders: [{ loader: "@next/font/google" }],
    appDir: true,
  },
};

module.exports = nextConfig;
