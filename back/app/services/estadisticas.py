from sqlalchemy import func, case, Integer
from sqlalchemy.orm import Session, aliased
from app.models.departamento import Departamentos
from app.models.municipio import Municipios
from app.models.vereda import Veredas
from app.models.puntoMuestreo import PuntosMuestreo
from app.models.resultado import Resultados


def listar_municipios_departamento(db: Session):
    # Realiza la consulta para obtener departamentos y municipios
    resultados = (
        db.query(Departamentos.Nombre.label("Departamento"), Municipios.Nombre.label("Municipio"))
        .join(Municipios, Municipios.Codigo_Departamento == Departamentos.Codigo)
        .all()
    )
    
    # Estructura los datos en el formato deseado
    departamentos_dict = {}
    for departamento, municipio in resultados:
        if departamento not in departamentos_dict:
            departamentos_dict[departamento] = {"departamento": departamento, "municipios": []}
        departamentos_dict[departamento]["municipios"].append({"nombre": municipio})
    
    # Devuelve los datos como lista de departamentos con sus municipios
    return list(departamentos_dict.values())

def obtener_resumen_irca(db: Session, anio_inicio, anio_fin, codigo_municipio):
    # Crear los alias para tablas si es necesario (opcional)
    m = Municipios
    v = Veredas
    pm = PuntosMuestreo 
    r = Resultados

    # Fecha_Toma is stored as text; derive year safely for PostgreSQL.
    year_expr = case(
        (func.substring(r.Fecha_Toma, 1, 4).op("~")(r"^[0-9]{4}$"), func.substring(r.Fecha_Toma, 1, 4).cast(Integer)),
        else_=None,
    )

    # Consulta con SQLAlchemy
    query = (
        db.query(
            m.Nombre.label("municipio"),
            m.Latitud.label("lat"),
            m.Longitud.label("lng"),
            year_expr.label("anio"),
            func.avg(r.IRCA).label("irca"),
            case(
                (func.avg(r.IRCA) > 80, "INVIABLE SANITARIAMENTE"),
                (func.avg(r.IRCA) > 35, "ALTO"),
                (func.avg(r.IRCA) > 14, "MEDIO"),
                (func.avg(r.IRCA) > 5, "BAJO"),
                else_="SIN RIESGO"
            ).label("estado")
        )
        .join(v, v.Codigo_Municipio == m.Codigo
        )
        .join(pm, pm.Codigo_Vereda == v.Codigo
        )
        .join(r, r.Codigo_Punto_Muestreo == pm.Codigo
        ).
        filter(
            year_expr.between(anio_inicio, anio_fin),
            m.Codigo == codigo_municipio if codigo_municipio else True
        )
        .group_by(
            m.Nombre,
            m.Latitud,
            m.Longitud,
            year_expr
        )
        .order_by(
            m.Nombre,
            year_expr
        )
    )

    resultados = query.all()

    municipios_dict = {}
    for municipio, lat, lng, anio, irca, estado in resultados:
        if municipio not in municipios_dict:
            municipios_dict[municipio] = {"municipio": municipio, "lat": lat, "lng": lng, "resultados": []}
        municipios_dict[municipio]["resultados"].append({"anio": anio, "irca": irca, "estado": estado})
    return list(municipios_dict.values())