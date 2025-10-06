-- phpMyAdmin SQL Dump
-- version 4.9.0.1
-- https://www.phpmyadmin.net/
--
-- Vært: sql100.infinityfree.com
-- Genereringstid: 06. 10 2025 kl. 09:41:24
-- Serverversion: 10.6.22-MariaDB
-- PHP-version: 7.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `if0_40103593_mlcrc`
--

-- --------------------------------------------------------

--
-- Struktur-dump for tabellen `race_laps`
--

CREATE TABLE `race_laps` (
  `lap_id` int(11) NOT NULL,
  `race_id` int(11) NOT NULL,
  `lap` int(11) NOT NULL,
  `driver_id` varchar(50) NOT NULL,
  `lap_time` time NOT NULL,
  `dif` float NOT NULL,
  `rank` int(11) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Begrænsninger for dumpede tabeller
--

--
-- Indeks for tabel `race_laps`
--
ALTER TABLE `race_laps`
  ADD PRIMARY KEY (`lap_id`);

--
-- Brug ikke AUTO_INCREMENT for slettede tabeller
--

--
-- Tilføj AUTO_INCREMENT i tabel `race_laps`
--
ALTER TABLE `race_laps`
  MODIFY `lap_id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
