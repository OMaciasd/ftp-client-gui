import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from ftplib import FTP


class ClienteFTP_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cliente FTP")

        # Variables de la interfaz
        self.host = tk.StringVar()
        self.usuario = tk.StringVar()
        self.contraseña = tk.StringVar()
        self.estado = tk.StringVar()

        # Set defaut Values.
        self.host.set("localhost")
        self.usuario.set("admin")
        self.contraseña.set("admin")

        # Conected Frame.
        frame_conexion = tk.LabelFrame(self.root, text="Conexión FTP")
        frame_conexion.pack(pady=20)

        # Conected Tags.
        tk.Label(frame_conexion, text="Host:").grid(
            row=0, column=0, padx=5, pady=5)
        tk.Entry(frame_conexion, textvariable=self.host).grid(
            row=0, column=1, padx=5, pady=5)

        tk.Label(frame_conexion, text="Usuario:").grid(
            row=1, column=0, padx=5, pady=5)
        tk.Entry(frame_conexion, textvariable=self.usuario).grid(
            row=1, column=1, padx=5, pady=5)

        tk.Label(frame_conexion, text="Contraseña:").grid(
            row=2, column=0, padx=5, pady=5)
        tk.Entry(frame_conexion, textvariable=self.contraseña,
                 show="*").grid(row=2, column=1, padx=5, pady=5)

        # Conected Buttons.
        tk.Button(frame_conexion, text="Conectar", command=self.conectar).grid(
            row=3, columnspan=2, padx=5, pady=10)

        # FTP Frame.
        frame_operaciones = tk.LabelFrame(self.root, text="Operaciones FTP")
        frame_operaciones.pack(pady=20)

        # FTP Actions Buttons.
        tk.Button(frame_operaciones, text="Listar Archivos",
                  command=self.listar_archivos).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(frame_operaciones, text="Subir Archivo",
                  command=self.subir_archivo).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(frame_operaciones, text="Eliminar Archivo",
                  command=self.eliminar_archivo).grid(row=0, column=2, padx=5, pady=5)

        # FTP State Tags.
        tk.Label(self.root, textvariable=self.estado, fg="blue").pack(pady=10)

        # FTP start.
        self.ftp = FTP()

    def conectar(self):
        try:
            host = self.host.get()
            usuario = self.usuario.get()
            contraseña = self.contraseña.get()

            self.ftp.connect(host)
            self.ftp.login(usuario, contraseña)

            self.estado.set(f"Conectado a {host}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar: {e}")

    def listar_archivos(self):
        try:
            archivos = self.ftp.nlst()
            messagebox.showinfo("Archivos en el servidor", "\n".join(archivos))
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo listar los archivos: {e}")

    def subir_archivo(self):
        try:
            archivo_local = filedialog.askopenfilename()
            if archivo_local:
                nombre_archivo = archivo_local.split("/")[-1]
                with open(archivo_local, 'rb') as f:
                    self.ftp.storbinary(f'STOR {nombre_archivo}', f)
                messagebox.showinfo("Éxito", f"Archivo '{
                                    nombre_archivo}' subido correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo subir el archivo: {e}")

    def eliminar_archivo(self):
        try:
            archivo_a_eliminar = simpledialog.askstring(
                "Eliminar archivo", "Ingrese el nombre del archivo a eliminar:")
            if archivo_a_eliminar:
                self.ftp.delete(archivo_a_eliminar)
                messagebox.showinfo("Éxito", f"Archivo '{
                                    archivo_a_eliminar}' eliminado correctamente")
        except Exception as e:
            messagebox.showerror(
                "Error", f"No se pudo eliminar el archivo: {e}")


# App run.
if __name__ == "__main__":
    root = tk.Tk()
    cliente_ftp_gui = ClienteFTP_GUI(root)
    root.mainloop()
