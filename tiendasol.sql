
DROP DATABASE IF EXISTS tiendadelsol;
CREATE DATABASE tiendadelsol;
USE tiendadelsol;

CREATE TABLE IF NOT EXISTS categorias (
  id_categoria INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  PRIMARY KEY (id_categoria)
) 

CREATE TABLE IF NOT EXISTS articulos (
  codigo CHAR(13) NOT NULL,
  nombre VARCHAR(100) NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  costo DECIMAL(10,2) NOT NULL,
  existencia INT NOT NULL,
  unidad VARCHAR(50) NULL DEFAULT NULL,
  descripcion TEXT NULL DEFAULT NULL,
  id_categoria INT NULL DEFAULT NULL,
  PRIMARY KEY (codigo),
  INDEX idx_categoria (id_categoria),
  CONSTRAINT articulos_ibfk_1 FOREIGN KEY (id_categoria) REFERENCES categorias (id_categoria)
) 


CREATE TABLE IF NOT EXISTS clientes (
  id_cliente INT NOT NULL AUTO_INCREMENT,
  telefono VARCHAR(15) NULL DEFAULT NULL,
  nombre VARCHAR(100) NOT NULL,
  direccion TEXT NULL DEFAULT NULL,
  rfc VARCHAR(13) NULL DEFAULT NULL,
  correo VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (id_cliente),
  UNIQUE INDEX unq_correo (correo)
) 


CREATE TABLE IF NOT EXISTS metodospago (
  id_metodo INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(50) NOT NULL,
  PRIMARY KEY (id_metodo)
) 

CREATE TABLE IF NOT EXISTS ventas (
  id_venta INT NOT NULL AUTO_INCREMENT,
  fecha DATETIME NOT NULL,
  id_cliente INT NULL DEFAULT NULL,
  id_metodo INT NULL DEFAULT NULL,
  PRIMARY KEY (id_venta),
  INDEX idx_cliente (id_cliente),
  INDEX idx_metodo (id_metodo),
  CONSTRAINT ventas_ibfk_1 FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
  CONSTRAINT ventas_ibfk_2 FOREIGN KEY (id_metodo) REFERENCES metodospago (id_metodo)
) 

CREATE TABLE IF NOT EXISTS detalle_ventas (
  id_detalle INT NOT NULL AUTO_INCREMENT,
  id_venta INT NULL DEFAULT NULL,
  codigo_articulo CHAR(13) NULL DEFAULT NULL,
  cantidad INT NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  importe DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_detalle),
  INDEX idx_venta (id_venta),
  INDEX idx_codigo_articulo (codigo_articulo),
  CONSTRAINT detalle_ventas_ibfk_1 FOREIGN KEY (id_venta) REFERENCES ventas (id_venta),
  CONSTRAINT detalle_ventas_ibfk_2 FOREIGN KEY (codigo_articulo) REFERENCES articulos (codigo)
)

CREATE TABLE IF NOT EXISTS empleados (
  id_empleado INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  cargo VARCHAR(50) NOT NULL,
  telefono VARCHAR(15) NULL DEFAULT NULL,
  correo VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (id_empleado),
  UNIQUE INDEX unq_empleado_correo (correo)
) 

CREATE TABLE IF NOT EXISTS garantias (
  id_garantia INT NOT NULL AUTO_INCREMENT,
  id_venta INT NULL DEFAULT NULL,
  codigo_articulo CHAR(13) NULL DEFAULT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  PRIMARY KEY (id_garantia),
  INDEX idx_garantia_venta (id_venta),
  INDEX idx_garantia_articulo (codigo_articulo),
  CONSTRAINT garantias_ibfk_1 FOREIGN KEY (id_venta) REFERENCES ventas (id_venta),
  CONSTRAINT garantias_ibfk_2 FOREIGN KEY (codigo_articulo) REFERENCES articulos (codigo)
) 

CREATE TABLE IF NOT EXISTS proveedores (
  id_proveedor INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(100) NOT NULL,
  telefono VARCHAR(15) NULL DEFAULT NULL,
  correo VARCHAR(100) NULL DEFAULT NULL,
  direccion TEXT NULL DEFAULT NULL,
  PRIMARY KEY (id_proveedor)
) 

CREATE TABLE IF NOT EXISTS proveedores_has_articulos (
  id_proveedor INT NOT NULL,
  codigo_articulo CHAR(13) NOT NULL,
  PRIMARY KEY (id_proveedor, codigo_articulo),
  INDEX idx_prov_articulo (codigo_articulo),
  CONSTRAINT fk_proveedor_articulo_prov FOREIGN KEY (id_proveedor) REFERENCES proveedores (id_proveedor),
  CONSTRAINT fk_proveedor_articulo_art FOREIGN KEY (codigo_articulo) REFERENCES articulos (codigo)
)
