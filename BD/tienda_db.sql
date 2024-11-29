-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 29-11-2024 a las 07:36:03
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_db`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `added_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `cart`
--

INSERT INTO `cart` (`id`, `user_id`, `product_id`, `quantity`, `added_at`) VALUES
(33, 1, 3, 2, '2024-11-29 00:56:51'),
(34, 1, 1, 6, '2024-11-29 01:28:35'),
(35, 1, 2, 1, '2024-11-29 06:22:22');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categories`
--

INSERT INTO `categories` (`id`, `name`, `created_at`) VALUES
(1, 'Luminaria', '2024-11-22 16:42:18'),
(2, 'Rosas externas', '2024-11-22 16:43:14'),
(3, 'Acrílico', '2024-11-28 15:27:17'),
(4, 'Emprendedores', '2024-11-28 15:27:40');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `company_social_networks`
--

CREATE TABLE `company_social_networks` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `network_name` varchar(255) NOT NULL,
  `network_url` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `company_social_networks`
--

INSERT INTO `company_social_networks` (`id`, `network_name`, `network_url`, `created_at`) VALUES
(1, 'Faceboop', 'https://www.facebook.com', '2024-11-29 04:36:36'),
(2, 'WhatsApp', 'https://web.whatsapp.com/', '2024-11-29 04:37:54'),
(3, 'Instagram', 'https://www.instagram.com/', '2024-11-29 04:56:32'),
(4, 'X', 'https://x.com/', '2024-11-29 04:58:10');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `info_companies`
--

CREATE TABLE `info_companies` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `info_companies`
--

INSERT INTO `info_companies` (`id`, `name`, `description`, `address`, `phone_number`, `email`, `created_at`, `updated_at`) VALUES
(1, 'tienda online', 'somos una tienda a pues si', 'av.berlin', '111111', 'info@mail.com', '2024-11-29 03:56:38', '2024-11-29 05:21:54');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `logos`
--

CREATE TABLE `logos` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `logos`
--

INSERT INTO `logos` (`id`, `name`, `image_url`, `updated_at`) VALUES
(1, 'Web Store ', 'uploads/png-transparent-e-commerce-2018-online-shopping-amazon-com-supermercado-text-retail-logo-removebg-preview.png', '2024-11-28 15:19:15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `delivery_date` date DEFAULT NULL,
  `delivery_location` varchar(255) DEFAULT NULL,
  `customer_name` varchar(255) DEFAULT NULL,
  `customer_phone` varchar(20) DEFAULT NULL,
  `delivery_time` varchar(50) DEFAULT NULL,
  `observation` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `orders`
--

INSERT INTO `orders` (`id`, `product_id`, `delivery_date`, `delivery_location`, `customer_name`, `customer_phone`, `delivery_time`, `observation`, `created_at`) VALUES
(1, 1, '2024-11-29', 'berlin usulutan', 'david', '77777777', '10:22', 'hola', '2024-11-28 22:28:20'),
(2, 3, '2024-11-29', 'berlin usulutan', 'david', '77777777', '10:22', 'hola', '2024-11-28 22:28:20'),
(3, 2, '2024-11-28', 'berlin usulutan', 'david', '77777777', '03:05', 'jajaj', '2024-11-28 23:05:47'),
(4, 2, '2024-11-29', 'berlin usulutan', 'david', '77777777', '21:08', 'jjjjj', '2024-11-28 23:08:38'),
(5, 4, '2024-11-29', 'berlin usulutan', 'david', '77777777', '21:08', 'jjjjj', '2024-11-28 23:08:38'),
(6, 1, '2024-11-30', 'berlin usulutan', 'alex', '00000000', '08:14', 'jjjj', '2024-11-28 23:14:52'),
(7, 3, '2024-11-30', 'berlin usulutan', 'alex', '00000000', '08:14', 'jjjj', '2024-11-28 23:14:52'),
(8, NULL, '2024-12-01', 'berlin usulutan', 'david', '77777777', '11:00', 'kkkk', '2024-11-29 00:00:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `product_id`, `quantity`) VALUES
(1, 1, 1, 2),
(2, 2, 3, 1),
(3, 3, 2, 1),
(4, 4, 2, 1),
(5, 5, 4, 1),
(6, 6, 1, 1),
(7, 7, 3, 1),
(8, 8, 3, 1),
(9, 8, 2, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `payment_system`
--

CREATE TABLE `payment_system` (
  `id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `payment_method` enum('tarjeta','transferencia') DEFAULT NULL,
  `payment_type` enum('POST','banco privado','banco nacional') DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `payment_system`
--

INSERT INTO `payment_system` (`id`, `order_id`, `payment_method`, `payment_type`, `created_at`) VALUES
(1, 1, '', '', '2024-11-28 22:28:20'),
(2, 2, '', '', '2024-11-28 22:28:20'),
(3, 3, '', '', '2024-11-28 23:05:47'),
(4, 4, '', '', '2024-11-28 23:08:38'),
(5, 5, '', '', '2024-11-28 23:08:38'),
(6, 6, '', '', '2024-11-28 23:14:52'),
(7, 7, '', '', '2024-11-28 23:14:52'),
(8, 8, '', '', '2024-11-29 00:00:31');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `category_id` int(11) DEFAULT NULL,
  `image_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `products`
--

INSERT INTO `products` (`id`, `name`, `description`, `price`, `stock`, `category_id`, `image_url`) VALUES
(1, 'Lampara', 'lampara moderna', 10.00, 2, 1, 'static/uploads\\lampara-de-mesa-.jpg'),
(2, 'Linterna', 'de techo', 15.00, 2, 1, 'https://hips.hearstapps.com/hmg-prod/images/lampra-stilnovo-1653552790.jpg?crop=0.753xw:1.00xh;0.124xw,0&resize=640:*'),
(3, 'Rosas ', 'externas', 20.00, 2, 2, 'https://i.pinimg.com/736x/c9/a8/71/c9a871195ddcd12914b55edd9f35e946.jpg'),
(4, 'flores', 'flores', 10.00, 2, 2, 'https://i.pinimg.com/736x/c9/a8/71/c9a871195ddcd12914b55edd9f35e946.jpg');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `quienes_somos`
--

CREATE TABLE `quienes_somos` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `image_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `quienes_somos`
--

INSERT INTO `quienes_somos` (`id`, `title`, `description`, `image_url`, `created_at`, `updated_at`) VALUES
(1, '¿Quienes Somos? ', 'Somos una tienda en línea comprometida con ofrecer productos únicos que combinan belleza, funcionalidad y calidad. Especializados en rosas externas, luminarias modernas y acrílicos personalizados, trabajamos para hacer de tus espacios algo realmente especial', 'uploads/eCommerce-logo.jpg', '2024-11-24 16:01:46', '2024-11-24 22:12:50');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password`, `role`, `created_at`) VALUES
(1, 'Alex', 'alex@gmail.com', '$2b$12$eQ3IBz3wAG1wThCPA0vsvOIThUetP2hWmWxAoRV1MpKQRa6ss2TCa', 'customer', '2024-11-22 16:47:54'),
(2, 'Admin', 'admin@tienda.com', '$2b$12$ih6ExqbYqDN8ri6cTpaLWer3VBPi2gPvdNKriZbgsIcmfHWLyku3G', 'admin', '2024-11-22 16:48:59'),
(3, 'pao', 'pao@gmail.com', '$2b$12$YKB2lnRp2D13J3Ni3B1ToOBgOGUoUOuVLobhYq8up0xvODtgU2wXy', 'customer', '2024-11-23 11:59:00'),
(5, 'adal', 'adalberto@gmail.com', '$2b$12$TU0wSLkotVsC95F/jmAZvOmVfdfRtCFgqwCrFjrXaNKveHodueTgW', 'customer', '2024-11-29 06:07:01');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `company_social_networks`
--
ALTER TABLE `company_social_networks`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `info_companies`
--
ALTER TABLE `info_companies`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `logos`
--
ALTER TABLE `logos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indices de la tabla `payment_system`
--
ALTER TABLE `payment_system`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indices de la tabla `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indices de la tabla `quienes_somos`
--
ALTER TABLE `quienes_somos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT de la tabla `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `company_social_networks`
--
ALTER TABLE `company_social_networks`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `info_companies`
--
ALTER TABLE `info_companies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `logos`
--
ALTER TABLE `logos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `payment_system`
--
ALTER TABLE `payment_system`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `quienes_somos`
--
ALTER TABLE `quienes_somos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Filtros para la tabla `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);

--
-- Filtros para la tabla `payment_system`
--
ALTER TABLE `payment_system`
  ADD CONSTRAINT `payment_system_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);

--
-- Filtros para la tabla `products`
--
ALTER TABLE `products`
  ADD CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
