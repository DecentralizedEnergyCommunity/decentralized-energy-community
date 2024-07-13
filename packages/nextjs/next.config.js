// @ts-check

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  webpack: config => {
    config.resolve.fallback = { fs: false, net: false, tls: false };
    config.externals.push("pino-pretty", "lokijs", "encoding");
    return config;
  },

  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://nodered.steganos.dev/:path*",
      },
    ];
  },
};

module.exports = nextConfig;
