
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.resultado import Resultados

def get_resultados(db: Session):
    query = db.query(
        func.coalesce(Resultados.Resultado_Color_Aparente, Resultados.Resultado_Color_Aparente_In_Situ)
            .label("resultado_Color_Aparente"),
        func.coalesce(Resultados.Diagnostico_Color_Aparente, Resultados.Diagnostico_Color_Aparente_In_Situ)
            .label("diagnostico_Color_Aparente"),
        func.coalesce(Resultados.Resultado_Turbiedad, Resultados.Resultado_Turbiedad_In_Situ)
            .label("resultado_Turbiedad"),
        func.coalesce(Resultados.Diagnostico_Turbiedad, Resultados.Diagnostico_Turbiedad_In_Situ)
            .label("diagnostico_Turbiedad"),
        func.coalesce(Resultados.Resultado_Ph, Resultados.Resultado_Ph_In_Situ)
            .label("resultado_Ph"),
        func.coalesce(Resultados.Diagnostico_Ph, Resultados.Diagnostico_Ph_In_Situ)
            .label("diagnostico_Ph"),
        func.coalesce(Resultados.Resultado_Cloro_Residual_Libre, Resultados.Resultado_Cloro_Residual_Libre_In_Situ)
            .label("resultado_Cloro_Residual_Libre"),
        func.coalesce(Resultados.Diagnostico_Cloro_Residual_Libre, Resultados.Diagnostico_Cloro_Residual_Libre_In_Situ)
            .label("diagnostico_Cloro_Residual_Libre"),
        Resultados.Resultado_Alcalinidad_Total,
        Resultados.Diagnostico_Alcalinidad_Total,
        Resultados.Resultado_Aluminio,
        Resultados.Diagnostico_Aluminio,
        Resultados.Resultado_Cloruros,
        Resultados.Diagnostico_Cloruros,
        Resultados.Resultado_COT,
        Resultados.Diagnostico_COT,
        Resultados.Resultado_Dureza_Total,
        Resultados.Diagnostico_Dureza_Total,
        Resultados.Resultado_Fosfatos,
        Resultados.Diagnostico_Fosfatos,
        Resultados.Resultado_Manganeso,
        Resultados.Diagnostico_Manganeso,
        Resultados.Resultado_Nitratos,
        Resultados.Diagnostico_Nitratos,
        Resultados.Resultado_Nitritos,
        Resultados.Diagnostico_Nitritos,
        Resultados.Resultado_Sulfatos,
        Resultados.Diagnostico_Sulfatos,
        Resultados.Resultado_Coliformes_Totales,
        Resultados.Diagnostico_Coliformes_Totales,
        Resultados.Resultado_E_Coli,
        Resultados.Diagnostico_E_Coli,
        Resultados.Resultado_Floruros,
        Resultados.Diagnostico_Floruros,
        Resultados.Resultado_Hierro_Total,
        Resultados.Diagnostico_Hierro_Total,
        Resultados.IRCA,
        Resultados.Nivel_Riesgo
    ).all()
    
    resultados = []
    
    for row in query:
        resultado = {
            "resultado_Color_Aparente": row.resultado_Color_Aparente,
            "diagnostico_Color_Aparente": row.diagnostico_Color_Aparente,
            "resultado_Turbiedad": row.resultado_Turbiedad,
            "diagnostico_Turbiedad": row.diagnostico_Turbiedad,
            "resultado_Ph": row.resultado_Ph,
            "diagnostico_Ph": row.diagnostico_Ph,
            "resultado_Cloro_Residual_Libre": row.resultado_Cloro_Residual_Libre,
            "diagnostico_Cloro_Residual_Libre": row.diagnostico_Cloro_Residual_Libre,
            "resultado_Alcalinidad_Total": row.Resultado_Alcalinidad_Total,
            "diagnostico_Alcalinidad_Total": row.Diagnostico_Alcalinidad_Total,
            "resultado_Aluminio": row.Resultado_Aluminio,
            "diagnostico_Aluminio": row.Diagnostico_Aluminio,
            "resultado_Cloruros": row.Resultado_Cloruros,
            "diagnostico_Cloruros": row.Diagnostico_Cloruros,
            "resultado_COT": row.Resultado_COT,
            "diagnostico_COT": row.Diagnostico_COT,
            "resultado_Dureza_Total": row.Resultado_Dureza_Total,
            "diagnostico_Dureza_Total": row.Diagnostico_Dureza_Total,
            "resultado_Fosfatos": row.Resultado_Fosfatos,
            "diagnostico_Fosfatos": row.Diagnostico_Fosfatos,
            "resultado_Manganeso": row.Resultado_Manganeso,
            "diagnostico_Manganeso": row.Diagnostico_Manganeso,
            "resultado_Nitratos": row.Resultado_Nitratos,
            "diagnostico_Nitratos": row.Diagnostico_Nitratos,
            "resultado_Nitritos": row.Resultado_Nitritos,
            "diagnostico_Nitritos": row.Diagnostico_Nitritos,
            "resultado_Sulfatos": row.Resultado_Sulfatos,
            "diagnostico_Sulfatos": row.Diagnostico_Sulfatos,
            "resultado_Coliformes_Totales": row.Resultado_Coliformes_Totales,
            "diagnostico_Coliformes_Totales": row.Diagnostico_Coliformes_Totales,
            "resultado_E_Coli": row.Resultado_E_Coli,
            "diagnostico_E_Coli": row.Diagnostico_E_Coli,
            "resultado_Floruros": row.Resultado_Floruros,
            "diagnostico_Floruros": row.Diagnostico_Floruros,
            "resultado_Hierro_Total": row.Resultado_Hierro_Total,
            "diagnostico_Hierro_Total": row.Diagnostico_Hierro_Total,
            "IRCA": row.IRCA,
            "nivel_Riesgo": row.Nivel_Riesgo
        }
        resultados.append(resultado)
    return resultados
