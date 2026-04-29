-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost:3306
-- Tiempo de generación: 28-01-2026 a las 21:51:39
-- Versión del servidor: 5.7.24
-- Versión de PHP: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ing_software`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE `cliente` (
  `IdCliente` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Telefono` varchar(15) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `Usuario_IdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`IdCliente`, `Nombre`, `Apellido`, `Telefono`, `Correo`, `Usuario_IdUsuario`) VALUES
(2, 'wertyui', 'wertyu', '12345', 'asdfgh', 8),
(3, 'asdfg', 'qwerty', '12345', 'asdfg', 9),
(4, 'qwdfgh', 'sdfgv', '123456', 'sdfvghbj', 10),
(5, 'qwertyuiop', 'qwertyuiop', '12345', 'wdwewrrvevetvetv', 12),
(7, 'Juan', 'gonzalez', '32212133', 'dscew@gmailcom', 16),
(8, 'joceline', 'de la torre', '317018100', 'joceline@gmail.com', 18),
(9, 'pedro', 'juan', '1234123451', '32223@gmail.com', 20),
(10, 'Ian', 'Ian', '1111111111', 'ianrara@gmai.com', 21),
(11, 'pedro', 'pedro', '2222222222', 'mwwce@gmail.com', 24),
(12, 'pitoloko', 'lloooooo', '2223323', 'lloooo@gmail.com', 26),
(13, 'cliente', 'cliente', '2345678563', 'cliente@gmail.com', 33),
(14, 'cliente10', 'cliente10', '2345678912', 'cliente10@gmail.com', 34),
(15, 'pedro24', 'pedro24', '1234567891', 'juanperez@gmail.com', 35),
(16, 'cliente13', 'cliente13', '1234567891', 'cliente12@gmail.com', 36),
(17, 'pepe', 'silvas', '3221231234', 'pepesilvas@gmail.com', 37);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cortecaja`
--

CREATE TABLE `cortecaja` (
  `idCorteCaja` int(11) NOT NULL,
  `Hora_Inicio` varchar(10) NOT NULL,
  `Hora_Terminar` varchar(10) NOT NULL,
  `Fecha_Inicio` varchar(10) NOT NULL,
  `DineroEnCaja` double NOT NULL,
  `IngresoDia` double NOT NULL,
  `EgresoDIa` double NOT NULL,
  `PlatillosVendidos` int(11) NOT NULL,
  `DineroFinalizar` double NOT NULL,
  `TiempoTrascurrido` int(11) NOT NULL,
  `FechaFinalizar` date NOT NULL,
  `Administrador_idAdministrador` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `cortecaja`
--

INSERT INTO `cortecaja` (`idCorteCaja`, `Hora_Inicio`, `Hora_Terminar`, `Fecha_Inicio`, `DineroEnCaja`, `IngresoDia`, `EgresoDIa`, `PlatillosVendidos`, `DineroFinalizar`, `TiempoTrascurrido`, `FechaFinalizar`, `Administrador_idAdministrador`) VALUES
(1, '07:40:55', '00:00', '2025-04-04', 390, 690, 500, 0, 0, 0, '2025-04-04', 1),
(2, '00:07:19', '00:00', '2026-01-11', 0, 0, 0, 0, 0, 0, '2026-01-11', 15),
(3, '16:50:03', '00:00', '2026-01-11', 0, 0, 0, 0, 0, 0, '2026-01-11', 15),
(4, '17:10:48', '00:00', '2026-01-11', 0, 0, 0, 0, 0, 0, '2026-01-11', 15),
(5, '17:11:12', '00:00', '2026-01-11', 0, 0, 0, 0, 0, 0, '2026-01-11', 15),
(6, '21:50:27', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(7, '21:54:52', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(8, '21:55:45', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(9, '22:16:47', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(10, '22:37:10', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(11, '22:43:22', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(12, '22:48:05', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(13, '23:20:11', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(14, '23:20:43', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(15, '23:37:58', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(16, '23:38:10', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(17, '23:38:15', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(18, '23:38:21', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(19, '23:38:37', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(20, '23:38:47', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(21, '23:39:24', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(22, '23:52:23', '00:00', '2026-01-13', 0, 0, 0, 0, 0, 0, '2026-01-13', 15),
(23, '00:26:23', '00:00', '2026-01-14', 0, 0, 0, 0, 0, 0, '2026-01-14', 15),
(24, '00:26:51', '00:00', '2026-01-14', 0, 0, 0, 0, 0, 0, '2026-01-14', 15);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalleventas`
--

CREATE TABLE `detalleventas` (
  `idDetalleVentas` int(11) NOT NULL,
  `Subtotal` float NOT NULL,
  `Impuesto` float NOT NULL,
  `Descuento` float NOT NULL,
  `Total` float NOT NULL,
  `Ventas_IdVentas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `detalleventas`
--

INSERT INTO `detalleventas` (`idDetalleVentas`, `Subtotal`, `Impuesto`, `Descuento`, `Total`, `Ventas_IdVentas`) VALUES
(1, 126, 24, 0, 150, 1),
(3, 126, 24, 0, 150, 3),
(4, 126, 24, 0, 150, 4),
(5, 126, 24, 0, 150, 5),
(6, 126, 24, 0, 150, 6),
(7, 126, 24, 0, 150, 7),
(8, 126, 24, 0, 150, 8),
(9, 126, 24, 0, 150, 9);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleado`
--

CREATE TABLE `empleado` (
  `IdEmpleado` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Telefono` varchar(15) NOT NULL,
  `Correo` varchar(100) NOT NULL,
  `Usuario_IdUsuario` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `empleado`
--

INSERT INTO `empleado` (`IdEmpleado`, `Nombre`, `Apellido`, `Telefono`, `Correo`, `Usuario_IdUsuario`) VALUES
(1, 'werty', 'ergh', '2342345', 'qwf', 7),
(2, 'qweryu', 'asdfgh', '1234567', 'asdfghj', 11),
(3, 'prueba', 'prueba', '123456789', 'pruebamail.com', 14),
(4, 'pedro', 'lopez', '322223324', 'lopezQgmail.com', 15),
(5, 'Emily', 'Villanueva', '322308474155677', 'emy@gmail.com', 17),
(6, 'Xavier Noel', 'Ibarra', '3223521446', 'xav@gmail.com', 19),
(7, 'Pedro', 'Pedro', '1222223345', 'pedro@gmail.com', 22),
(8, 'pedro', 'juan', '2222222222', 'ian@gmail.com', 23),
(9, 'juan', 'defew', '1234563454', 'aweew@gmail.com', 25),
(10, 'pitoeewefwefwe1234', 'wetyuikjvcxaertyjnbvdw', '12345678924', 'juancho@gmail.com', 27),
(12, 'pitoeewefwefwe1234', 'wetyuikjvcxaertyjnbvdw', '12345678924', 'juancho122332@gmail.com', 29),
(14, 'user', 'user', '1234567864', 'user@gmail.com', 32),
(15, 'User', 'Diez', '0000000000', 'user10@gmail.com', 31);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradarecibe`
--

CREATE TABLE `entradarecibe` (
  `IdEntradaProductoa` int(11) NOT NULL,
  `FechaRecibo` date NOT NULL,
  `EmpleadoRecibio` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entradasproductos`
--

CREATE TABLE `entradasproductos` (
  `IdEntradasProductos` int(11) NOT NULL,
  `Cantidad` int(11) NOT NULL,
  `Fecha` date NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `entradasproductos`
--

INSERT INTO `entradasproductos` (`IdEntradasProductos`, `Cantidad`, `Fecha`, `Descripcion`, `CorteCaja_idCorteCaja`) VALUES
(1, 2, '2025-03-12', '122', 1),
(2, 2, '2025-03-12', '122', 1),
(3, 12, '2025-03-12', 'acda', 1),
(4, 212, '2025-04-05', '121', 1),
(5, 212, '2025-04-05', '121', 1),
(15, 212, '2025-04-05', '12', 1),
(16, 12, '2025-04-05', 'wwew', 1),
(17, -6, '2025-04-10', 'ENTRADA DE COCA COLA', 1),
(18, 2, '2025-05-06', 'jojojo', 1),
(19, 12, '2025-05-06', '34', 1),
(20, 22, '2025-05-10', 'eef', 1),
(21, 10, '2025-12-13', '4|cola|noooo', 1),
(22, 100, '2025-12-16', '7|prueba|soo', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estatuspedido`
--

CREATE TABLE `estatuspedido` (
  `IdEstatusPedido` int(11) NOT NULL,
  `SituacionPedido` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `estatuspedido`
--

INSERT INTO `estatuspedido` (`IdEstatusPedido`, `SituacionPedido`) VALUES
(1, 'Pagado'),
(2, 'Pagado'),
(3, 'Pedido Realizado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarpedido`
--

CREATE TABLE `generarpedido` (
  `IdGenerarPedido` int(11) NOT NULL,
  `HoraPedido` time NOT NULL,
  `FechaPedido` date NOT NULL,
  `Producto` varchar(500) DEFAULT NULL,
  `Total` decimal(10,2) DEFAULT NULL,
  `NumeroMesa` int(11) NOT NULL,
  `Estatus` varchar(20) NOT NULL,
  `EstatusPedido_IdEstatusPedido` int(11) NOT NULL,
  `Clientes_Idcliente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `generarpedido`
--

INSERT INTO `generarpedido` (`IdGenerarPedido`, `HoraPedido`, `FechaPedido`, `Producto`, `Total`, `NumeroMesa`, `Estatus`, `EstatusPedido_IdEstatusPedido`, `Clientes_Idcliente`) VALUES
(32, '23:01:28', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', 1, 'Pagado', 3, 1),
(33, '23:01:28', '2025-05-11', 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', 1, 'Pagado', 3, 1),
(34, '23:01:28', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', 1, 'Pagado', 3, 1),
(35, '23:21:24', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', 1, 'Pagado', 3, 1),
(36, '23:21:24', '2025-05-11', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', 1, 'Pagado', 3, 1),
(37, '20:44:46', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', 1, 'Pagado', 3, 1),
(38, '20:44:46', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', 1, 'Pagado', 3, 1),
(39, '22:12:14', '2025-05-12', 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Papas Fritas, Guacamole $10', '150.00', 1, 'Pagado', 3, 1),
(43, '15:43:27', '2025-05-14', '4 comensales | Pizza Hawaiana (2) - sc', '240.00', 7, 'Pagado', 3, 1),
(44, '15:48:23', '2025-05-14', '2 comensales | Hamburguesa BBQ (1) - ww', '150.00', 6, 'Pedido Realizado', 3, 1),
(46, '15:58:49', '2025-05-14', '2 comensales | Hamburguesa BBQ (1) - 22', '150.00', 6, 'Pedido Realizado', 3, 1),
(47, '16:28:24', '2025-05-14', '2 comensales | Pizza Hawaiana (11) - dw', '1320.00', 3, 'Pedido Realizado', 3, 1),
(48, '21:35:46', '2025-12-28', 'Té Boba Fresa (x1) [Tamaño: Mediano | Azúcar: 70% | Hielo: 70% | Leche: Entera]', '59.00', 1, 'Pedido Realizado', 3, 1),
(49, '22:26:46', '2026-01-14', 'Té Boba Fresa (x1) [Tamaño: Mediano | Azúcar: 50% | Hielo: 70% | Leche: Entera | Extras: Jelly]', '65.00', 1, 'Pedido Realizado', 3, 1),
(50, '16:47:41', '2026-01-26', 'Frappé Mocha (x1) [Tamaño: Mediano | Azúcar: 20% | Hielo: 50% | Leche: Entera | Extras: Crema | Notas: que lo traiga una chichona por favor]', '81.00', 1, 'Pedido Realizado', 3, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `generarrecibo`
--

CREATE TABLE `generarrecibo` (
  `IdGenerarRecibo` int(11) NOT NULL,
  `FechaRecibo` varchar(45) NOT NULL,
  `HoraRecibo` varchar(45) NOT NULL,
  `descripcion` varchar(45) NOT NULL,
  `Ventas_IdVentas` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ingresos_egresos`
--

CREATE TABLE `ingresos_egresos` (
  `idMovimiento` int(11) NOT NULL,
  `TipoMovimiento` varchar(20) DEFAULT NULL,
  `Monto` decimal(10,2) DEFAULT NULL,
  `Descripcion` text,
  `Fecha` date DEFAULT NULL,
  `Hora` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ingresos_egresos`
--

INSERT INTO `ingresos_egresos` (`idMovimiento`, `TipoMovimiento`, `Monto`, `Descripcion`, `Fecha`, `Hora`) VALUES
(1, 'Ingreso', '12.00', 'sd', '2025-12-18', '20:58:33');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `IdProductos` int(11) NOT NULL,
  `Nombre` varchar(30) NOT NULL,
  `Precio` double NOT NULL,
  `FechaCaducidad` int(11) NOT NULL,
  `Descripcion` varchar(45) NOT NULL,
  `Marca` varchar(25) NOT NULL,
  `UnidadMedida` varchar(25) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`IdProductos`, `Nombre`, `Precio`, `FechaCaducidad`, `Descripcion`, `Marca`, `UnidadMedida`, `CorteCaja_idCorteCaja`) VALUES
(1, 'wefgh', 12, 111234, 'sdfghj', 'ml', 'mm', 1),
(2, 'mewpe', 12, 112234, 'asdf', 'jumex', 'mm', 1),
(3, 'efe', 232, 12, '3232', '2312', '23', 1),
(4, 'COCA COLA', 324234324132, 20250823, 'REFRESCO QUE LE GUSTA A ELIAS', 'PEPSI COLA', 'PIEZAS', 1),
(5, 'cola', 23, 12032022, 'hola', 'jkjkjlk', '2', 1),
(6, 'cec', 1121, 11111111, 'dss', '33', 'wdawd', 1),
(7, 'wefw', 111.22, 22222222, 'awfafwf', 'qfwfe', 've', 1),
(8, 'prueba', 10, 20040820, 'agua', 'marca', 'so', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productosstock`
--

CREATE TABLE `productosstock` (
  `IdProductosStock` int(11) NOT NULL,
  `Nombre` varchar(45) NOT NULL,
  `Descripcion` varchar(35) NOT NULL,
  `Cantidad` int(11) NOT NULL DEFAULT '0',
  `CorteCaja_idCorteCaja` int(11) NOT NULL,
  `Apariencia` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `productosstock`
--

INSERT INTO `productosstock` (`IdProductosStock`, `Nombre`, `Descripcion`, `Cantidad`, `CorteCaja_idCorteCaja`, `Apariencia`) VALUES
(1, 'wefgh', 'sdfghj', 211, 1, NULL),
(2, 'mewpe', 'asdf', 10, 1, NULL),
(4, 'cola', 'hola', 11, 1, NULL),
(5, 'wefw', 'awfafwf', 22, 1, NULL),
(6, 'pedro', 'sefse', 0, 1, 'efew'),
(7, 'prueba', 'agua', 100, 1, NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibos`
--

CREATE TABLE `recibos` (
  `idRecibo` int(11) NOT NULL,
  `Producto` varchar(255) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `Usuario` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `recibos`
--

INSERT INTO `recibos` (`idRecibo`, `Producto`, `Total`, `Fecha`, `Hora`, `Usuario`) VALUES
(1, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:32', 'Invitado'),
(2, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(3, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(4, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(5, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(6, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:34', 'Invitado'),
(7, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(8, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(9, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(10, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(11, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:35', 'Invitado'),
(12, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:36', 'Invitado'),
(13, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:36', 'Invitado'),
(14, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:37', 'Invitado'),
(15, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:37', 'Invitado'),
(16, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(17, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(18, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(19, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(20, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(21, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:38', 'Invitado'),
(22, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(23, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(24, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(25, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-13', '11:59:39', 'Invitado'),
(26, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:04', 'Invitado'),
(27, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:05', 'Invitado'),
(28, 'Hamburguesa BBQ - Ingredientes: Doble Carne, Con Queso, Extra Salsa BBQ, Con Tocino, Sin Lechuga y Jitomate, Con Papas, Chica, Ensalada, Salsa Picante', '180.00', '2025-05-13', '12:02:05', 'Invitado'),
(29, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:10', 'Invitado'),
(30, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(31, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(32, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:11', 'Invitado'),
(33, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(34, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(35, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(36, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:12', 'Invitado'),
(37, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(38, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(39, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(40, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:13', 'Invitado'),
(41, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(42, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(43, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(44, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(45, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:14', 'Invitado'),
(46, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(47, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(48, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(49, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:11:15', 'Invitado'),
(50, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:40:58', 'Invitado'),
(51, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:03', 'Invitado'),
(52, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:04', 'Invitado'),
(53, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:04', 'Invitado'),
(54, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:14', 'Invitado'),
(55, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:15', 'Invitado'),
(56, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:16', 'Invitado'),
(57, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(58, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(59, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:17', 'Invitado'),
(60, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:28', 'Invitado'),
(61, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:29', 'Invitado'),
(62, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:29', 'Invitado'),
(63, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:29', 'Invitado'),
(64, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:30', 'Invitado'),
(65, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:30', 'Invitado'),
(66, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:30', 'Invitado'),
(67, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(68, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(69, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(70, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:31', 'Invitado'),
(71, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Salsa Picante $10', '150.00', '2025-05-13', '12:41:32', 'Invitado'),
(72, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:32', 'Invitado'),
(73, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada', '140.00', '2025-05-13', '12:41:33', 'Invitado'),
(74, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(75, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(76, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:33', 'Invitado'),
(77, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Ensalada, Salsa Picante', '150.00', '2025-05-13', '12:41:34', 'Invitado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recibospedidos`
--

CREATE TABLE `recibospedidos` (
  `IdRecibosPedidos` int(11) NOT NULL,
  `Producto` varchar(255) NOT NULL,
  `Total` decimal(10,2) NOT NULL,
  `Fecha` date NOT NULL,
  `Hora` time NOT NULL,
  `Usuario` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `recibospedidos`
--

INSERT INTO `recibospedidos` (`IdRecibosPedidos`, `Producto`, `Total`, `Fecha`, `Hora`, `Usuario`) VALUES
(1, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Chica, Papas Fritas, Guacamole $10', '150.00', '2025-05-14', '03:04:35', 'Invitado'),
(2, 'Pizza Hawaiana - Ingredientes: Pina, Jamón, Queso, Mediana, Ensalada, Guacamole', '150.00', '2025-05-14', '03:25:36', 'Invitado'),
(3, '4 comensales | Pizza Hawaiana (2) - sc', '240.00', '2025-05-14', '16:14:01', 'Empleado'),
(4, 'Té Boba Fresa (x1) [Tamaño: Mediano | Azúcar: 70% | Hielo: 70% | Leche: Entera]', '59.00', '2025-12-28', '21:35:46', 'cliente13'),
(5, 'Té Boba Fresa (x1) [Tamaño: Mediano | Azúcar: 50% | Hielo: 70% | Leche: Entera | Extras: Jelly]', '65.00', '2026-01-14', '22:26:46', 'cliente13'),
(6, 'Frappé Mocha (x1) [Tamaño: Mediano | Azúcar: 20% | Hielo: 50% | Leche: Entera | Extras: Crema | Notas: que lo traiga una chichona por favor]', '81.00', '2026-01-26', '16:47:41', 'pepe');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `salidasproductos`
--

CREATE TABLE `salidasproductos` (
  `IdSalidasProductos` int(11) NOT NULL,
  `FechaSalida` date NOT NULL,
  `Detalle` varchar(45) NOT NULL,
  `Cantidad` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `salidasproductos`
--

INSERT INTO `salidasproductos` (`IdSalidasProductos`, `FechaSalida`, `Detalle`, `Cantidad`, `CorteCaja_idCorteCaja`) VALUES
(1, '2025-03-12', '22', '11', NULL),
(2, '2025-04-05', 'ee', '2.0', 1),
(3, '2025-05-06', 'jshjhs', '1.0', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipossalidas`
--

CREATE TABLE `tipossalidas` (
  `idTiposSalidas` int(11) NOT NULL,
  `ConceptoSalida` varchar(45) NOT NULL,
  `SalidasProductos_IdSalidasProductos` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `IdUsuario` int(11) NOT NULL,
  `NombreUsuario` varchar(45) NOT NULL,
  `Contraseña` varchar(79) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `usuario`
--

INSERT INTO `usuario` (`IdUsuario`, `NombreUsuario`, `Contraseña`) VALUES
(2, 'eertyre', 'wert'),
(6, 'qwedf_c', 'cliente123'),
(7, 'werty_e', 'empleado123'),
(8, 'wertyui_c', 'cliente123'),
(9, 'qqqqqqqqqq', 'qwer'),
(10, 'pppppppppp', 'werh'),
(11, 'yyyyyyyy', 'qwet'),
(12, 'tttttttttt', '11111'),
(14, 'prueba', '123'),
(15, 'lopez', '123'),
(16, 'pedro', '123'),
(17, 'Emikukis', 'Emikukis'),
(18, 'joce', '123'),
(19, 'Xavier2024', 'Xavier12'),
(20, '123', '1234567'),
(21, 'Ian', '5dfaaebff3e8ec0b796b47c7c674652150d92a16837946220d7efea32b8a854d'),
(22, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918'),
(23, 'mark', 'db55da3fc3098e9c42311c6013304ff36b19ef73d12ea932054b5ad51df4f49d'),
(24, 'pedro222', '36a2c3d76ddd529523197f3cdd8170223b800bfed6f27c56aabbd5092d8c7821'),
(25, 'juan', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'),
(26, 'pedroricko', 'pedro'),
(27, 'putaslokas', 'hola'),
(29, 'putaslokas121312', 'hola'),
(30, 'pecas', 'pecas'),
(31, 'user10', 'user10'),
(32, 'user20', 'user20'),
(33, 'cliente10', 'cliente10'),
(34, 'cliente12', 'cliente10'),
(35, 'juanperez@gmail.com', 'pedro24'),
(36, 'cliente13', 'cliente13'),
(37, 'pepe', 'pepe2020');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `IdVentas` int(11) NOT NULL,
  `Hora` varchar(45) NOT NULL,
  `FechaVenta` date NOT NULL,
  `DetalleVenta` varchar(45) NOT NULL,
  `CorteCaja_idCorteCaja` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`IdVentas`, `Hora`, `FechaVenta`, `DetalleVenta`, `CorteCaja_idCorteCaja`) VALUES
(1, '05:20:05', '2025-04-09', 'Hamburguesa BBQ (Extra Salsa BBQ)', 1),
(3, '23:07:53', '2025-04-09', 'Pizza Hawaiana (Jamón)', 1),
(4, '23:07:57', '2025-04-09', 'Hamburguesa BBQ (Doble Carne)', 1),
(5, '23:07:59', '2025-04-09', 'Pizza Hawaiana (Jamón)', 1),
(6, '23:08:00', '2025-04-09', 'Hamburguesa BBQ (Sin Lechuga y Jitomate)', 1),
(7, '23:08:03', '2025-04-09', 'Tacos al Pastor (Cilantro)', 1),
(8, '16:47:06', '2025-04-10', 'wdqw (dwa) - wdw', 1),
(9, '16:47:20', '2025-04-10', '3 comensales | Pizza Hawaiana (1) - muuj', 1);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`IdCliente`),
  ADD UNIQUE KEY `Correo` (`Correo`),
  ADD KEY `Usuario_IdUsuario` (`Usuario_IdUsuario`);

--
-- Indices de la tabla `cortecaja`
--
ALTER TABLE `cortecaja`
  ADD PRIMARY KEY (`idCorteCaja`),
  ADD KEY `fk_CorteCaja_Administrador1_idx` (`Administrador_idAdministrador`);

--
-- Indices de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD PRIMARY KEY (`idDetalleVentas`),
  ADD KEY `fk_DetalleVentas_Ventas1_idx` (`Ventas_IdVentas`);

--
-- Indices de la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD PRIMARY KEY (`IdEmpleado`),
  ADD UNIQUE KEY `Correo` (`Correo`),
  ADD KEY `Usuario_IdUsuario` (`Usuario_IdUsuario`);

--
-- Indices de la tabla `entradarecibe`
--
ALTER TABLE `entradarecibe`
  ADD PRIMARY KEY (`IdEntradaProductoa`),
  ADD KEY `fk_EntradaRecibe_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  ADD PRIMARY KEY (`IdEntradasProductos`),
  ADD KEY `fk_EntradasProductos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  ADD PRIMARY KEY (`IdEstatusPedido`);

--
-- Indices de la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  ADD PRIMARY KEY (`IdGenerarPedido`),
  ADD KEY `fk_GenerarPedido_EstatusPedido2_idx` (`EstatusPedido_IdEstatusPedido`),
  ADD KEY `fk_GenerarPedido_Clientes1_idx` (`Clientes_Idcliente`);

--
-- Indices de la tabla `generarrecibo`
--
ALTER TABLE `generarrecibo`
  ADD PRIMARY KEY (`IdGenerarRecibo`),
  ADD KEY `fk_GenerarRecibo_Ventas1_idx` (`Ventas_IdVentas`);

--
-- Indices de la tabla `ingresos_egresos`
--
ALTER TABLE `ingresos_egresos`
  ADD PRIMARY KEY (`idMovimiento`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`IdProductos`),
  ADD KEY `fk_Productos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `productosstock`
--
ALTER TABLE `productosstock`
  ADD PRIMARY KEY (`IdProductosStock`),
  ADD KEY `fk_ProductosStock_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `recibos`
--
ALTER TABLE `recibos`
  ADD PRIMARY KEY (`idRecibo`);

--
-- Indices de la tabla `recibospedidos`
--
ALTER TABLE `recibospedidos`
  ADD PRIMARY KEY (`IdRecibosPedidos`);

--
-- Indices de la tabla `salidasproductos`
--
ALTER TABLE `salidasproductos`
  ADD PRIMARY KEY (`IdSalidasProductos`),
  ADD KEY `fk_SalidasProductos_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- Indices de la tabla `tipossalidas`
--
ALTER TABLE `tipossalidas`
  ADD PRIMARY KEY (`idTiposSalidas`),
  ADD KEY `fk_TiposSalidas_SalidasProductos1_idx` (`SalidasProductos_IdSalidasProductos`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`IdUsuario`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`IdVentas`),
  ADD KEY `fk_Ventas_CorteCaja1_idx` (`CorteCaja_idCorteCaja`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `IdCliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `cortecaja`
--
ALTER TABLE `cortecaja`
  MODIFY `idCorteCaja` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  MODIFY `idDetalleVentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `empleado`
--
ALTER TABLE `empleado`
  MODIFY `IdEmpleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `entradasproductos`
--
ALTER TABLE `entradasproductos`
  MODIFY `IdEntradasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT de la tabla `estatuspedido`
--
ALTER TABLE `estatuspedido`
  MODIFY `IdEstatusPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  MODIFY `IdGenerarPedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;

--
-- AUTO_INCREMENT de la tabla `ingresos_egresos`
--
ALTER TABLE `ingresos_egresos`
  MODIFY `idMovimiento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `IdProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `productosstock`
--
ALTER TABLE `productosstock`
  MODIFY `IdProductosStock` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `recibos`
--
ALTER TABLE `recibos`
  MODIFY `idRecibo` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=78;

--
-- AUTO_INCREMENT de la tabla `recibospedidos`
--
ALTER TABLE `recibospedidos`
  MODIFY `IdRecibosPedidos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `salidasproductos`
--
ALTER TABLE `salidasproductos`
  MODIFY `IdSalidasProductos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `IdUsuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `IdVentas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD CONSTRAINT `cliente_ibfk_1` FOREIGN KEY (`Usuario_IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `detalleventas`
--
ALTER TABLE `detalleventas`
  ADD CONSTRAINT `fk_DetalleVentas_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`);

--
-- Filtros para la tabla `empleado`
--
ALTER TABLE `empleado`
  ADD CONSTRAINT `empleado_ibfk_1` FOREIGN KEY (`Usuario_IdUsuario`) REFERENCES `usuario` (`IdUsuario`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `entradarecibe`
--
ALTER TABLE `entradarecibe`
  ADD CONSTRAINT `fk_EntradaRecibe_CorteCaja1` FOREIGN KEY (`CorteCaja_idCorteCaja`) REFERENCES `cortecaja` (`idCorteCaja`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `generarpedido`
--
ALTER TABLE `generarpedido`
  ADD CONSTRAINT `fk_GenerarPedido_EstatusPedido2` FOREIGN KEY (`EstatusPedido_IdEstatusPedido`) REFERENCES `estatuspedido` (`IdEstatusPedido`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Filtros para la tabla `generarrecibo`
--
ALTER TABLE `generarrecibo`
  ADD CONSTRAINT `fk_GenerarRecibo_Ventas1` FOREIGN KEY (`Ventas_IdVentas`) REFERENCES `ventas` (`IdVentas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
