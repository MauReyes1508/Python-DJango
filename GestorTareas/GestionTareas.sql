-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-05-2024 a las 17:31:31
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

--
-- Volcado de datos para la tabla `tareas`
--

INSERT INTO `tareas` (`id_Tareas`, `Nombre`, `Fecha_Inicio`, `Fecha_final`, `Estado`) VALUES
(61, 'Ejercicio', '2024-05-14 10:16:00', '2024-05-15 10:16:00', 'Asignado');

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
  `ROL` varchar(15) NOT NULL,
  `Genero` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`id_user`, `Nombre`, `Apellido`, `User`, `Email`, `Contraseña`, `ROL`, `Genero`) VALUES
(1, 'Mauricio', 'Reyes', 'Mau1508', 'negrohamazuka@gmail.com\r\n', 'scrypt:32768:8:1$JKZcI1TfixoYdtuF$67c4128cb4154c6d464d56e797aa659562cc517234a467872b3ab83a77e27012dbfb0bb6aab573a1d76b547c8db879924b758183d6ac00ccf8906a94e93bb40c', 'admin', 'Masculino'),
(3, 'Nataly', 'Polo', 'Natt', 'natalyreyes@gmail.com', 'scrypt:32768:8:1$9JNOXbRVMAESVeTr$4fab6dadab2e6084b5d29ce6f3d6f8267b6cc795b328c6da6edd7d599b0b0a324a3e7011b9a394e869df3841bfe7376d91fd2edc504f744199685716960a5bbd', 'admin', 'Femenino'),
(4, 'Raúl', 'Reyes', 'Rauww15', 'Rauw@gmail.com', 'scrypt:32768:8:1$FRiapWb7JnwSBhRS$6185ee468d26e7c12f750df76f934f31e28f6106722bec808fed8a56bfe10b1924495c7a260c53175d193905ad63dff7b47c2fe4d9598aeb052d9d713ae0207a', 'usuario', 'Masculino');

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
  MODIFY `id_Tareas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=66;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
