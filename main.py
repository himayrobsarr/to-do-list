import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import json

# Configuración de la base de datos
Base = declarative_base()
engine = create_engine('sqlite:///tareas.db', echo=True)
Session = sessionmaker(bind=engine)

# Modelo de datos
class Tarea(Base):
    __tablename__ = 'tareas'
    
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)
    descripcion = Column(String(500))
    completada = Column(Boolean, default=False)

# Crear tablas
Base.metadata.create_all(engine)

# Funciones CRUD
def agregar_tarea(titulo, descripcion):
    session = Session()
    try:
        nueva_tarea = Tarea(titulo=titulo, descripcion=descripcion)
        session.add(nueva_tarea)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def listar_tareas():
    session = Session()
    try:
        return session.query(Tarea).all()
    finally:
        session.close()

def marcar_completada(tarea_id):
    session = Session()
    try:
        tarea = session.query(Tarea).filter_by(id=tarea_id).first()
        if tarea:
            tarea.completada = True
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

def eliminar_tarea(tarea_id):
    session = Session()
    try:
        tarea = session.query(Tarea).filter_by(id=tarea_id).first()
        if tarea:
            session.delete(tarea)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        return False
    finally:
        session.close()

# Interfaz de Streamlit
def main():
    st.title("Gestión de Tareas")
    
    # Menú lateral
    menu = st.sidebar.selectbox(
        "Seleccione una opción",
        ["Agregar Tarea", "Listar Tareas", "Exportar/Importar"]
    )
    
    if menu == "Agregar Tarea":
        st.subheader("Agregar Nueva Tarea")
        titulo = st.text_input("Título")
        descripcion = st.text_area("Descripción")
        
        if st.button("Agregar"):
            if titulo:
                if agregar_tarea(titulo, descripcion):
                    st.success("Tarea agregada exitosamente")
                else:
                    st.error("Error al agregar la tarea")
            else:
                st.warning("El título es obligatorio")
    
    elif menu == "Listar Tareas":
        st.subheader("Lista de Tareas")
        tareas = listar_tareas()
        
        for tarea in tareas:
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{tarea.titulo}**")
                st.write(tarea.descripcion)
                st.write("Estado: ✅" if tarea.completada else "Estado: ⏳")
            
            with col2:
                if not tarea.completada:
                    if st.button("Completar", key=f"comp_{tarea.id}"):
                        marcar_completada(tarea.id)
                        st.rerun()
            
            with col3:
                if st.button("Eliminar", key=f"del_{tarea.id}"):
                    eliminar_tarea(tarea.id)
                    st.rerun()
            
            st.markdown("---")
    
    elif menu == "Exportar/Importar":
        st.subheader("Exportar/Importar Tareas")
        
        if st.button("Exportar Tareas"):
            tareas = listar_tareas()
            datos = [{"id": t.id, "titulo": t.titulo, "descripcion": t.descripcion, 
                     "completada": t.completada} for t in tareas]
            
            st.download_button(
                label="Descargar JSON",
                data=json.dumps(datos, indent=2),
                file_name="tareas.json",
                mime="application/json"
            )
        
        archivo = st.file_uploader("Importar tareas desde JSON", type="json")
        if archivo is not None:
            try:
                datos = json.load(archivo)
                session = Session()
                for tarea_data in datos:
                    nueva_tarea = Tarea(
                        titulo=tarea_data["titulo"],
                        descripcion=tarea_data["descripcion"],
                        completada=tarea_data["completada"]
                    )
                    session.add(nueva_tarea)
                session.commit() 
                session.close()
                st.success("Tareas importadas exitosamente")
            except Exception as e:
                st.error(f"Error al importar tareas: {str(e)}")

if __name__ == "__main__":
    main()  


