-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-04-2024 a las 20:39:36
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestiontareas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tareas`
--

CREATE TABLE `tareas` (
  `id_Tareas` int(11) NOT NULL,
  `Nombre` varchar(200) NOT NULL,
  `Fecha_Inicio` datetime DEFAULT NULL,
  `Fecha_final` datetime DEFAULT NULL,
  `Estado` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id_user` int(11) NOT NULL,
  `Nombre` varchar(255) NOT NULL,
  `Apellido` varchar(255) NOT NULL,
  `User` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Contraseña` varchar(255) NOT NULL,
  `ROL` set('admin','usuario') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_user`, `Nombre`, `Apellido`, `User`, `Email`, `Contraseña`, `ROL`) VALUES
(1, 'Mauricio', 'Reyes', 'Mau1508', 'maurey@gmail.com', 'scrypt:32768:8:1$JKZcI1TfixoYdtuF$67c4128cb4154c6d464d56e797aa659562cc517234a467872b3ab83a77e27012dbfb0bb6aab573a1d76b547c8db879924b758183d6ac00ccf8906a94e93bb40c', 'admin'),
(2, 'Raúl', 'Manrique', 'Rauw15', 'RauMan26@gmail.com', 'scrypt:32768:8:1$Wy2kIUA3NEbJIpnK$3e62ea6b3491bdebf2e033b297b71e8379a8dfba272231bd1d764e9145ef100270d53d96d5564fde8316f9e94c07839ca06aaf691f33121ff3bbc00ff5d1d68f', 'usuario');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `tareas`
--
ALTER TABLE `tareas`
  ADD PRIMARY KEY (`id_Tareas`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `tareas`
--
ALTER TABLE `tareas`
  MODIFY `id_Tareas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=60;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
