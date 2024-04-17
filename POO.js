class Persona
{
    //Definir atributos de la clase.
    constructor(nombre, apellido, edad, genero, nacimiento)
    {
        this.Nombre = nombre;
        this.Apellido = apellido;
        this.Edad = edad;
        this.Genero = genero;
        this.Birth = nacimiento;
    }

    //Definir Métodos.

Saludar()
{
    console.log(`Buenos días. Soy  ${this.Nombre} ` );

}

Mayor()
{
    if (this.Edad >= 18)
    {
        console.log('Eres mayor de edad. ')
    }
    else
    {
        console.log('Eres mayor de edad. ')
    }
}

Menor()
{
    if (this.Edad < 18)
    {
        console.log('Eres menor de edad. ')
    }

    console.log('En mis tiempos, en los años 1600, ♪Tin ♪Tin ♪Tin. ')
}

Edad_En_Dias()
{
    let Years = Math.floor(this.Edad);
    let Days = Math.floor(this.Edad * 365);
    console.log(`Su merced ${this.Nombre} tiene: ${Years} años. `);
    console.log(`Su merced ${this.Nombre} tiene: ${Days} días de vida. `);
}

Edad_En_Meses()
{
    let Meses = Math.floor(this.Edad * 12);
    console.log(`Su merced ${this.Nombre} tiene: ${Meses} meses de vida. `);
}

}

//Creando un objeto.
const Persona1 = new Persona('Juan', 'Correa', 90, 'Masculino', 1934);
const Persona2 = new Persona('Daniel', 'Cruz', 18, 'Masculino', 2005);

Persona1.Saludar();
Persona2.Saludar();
Persona1.Mayor();
Persona2.Mayor();
Persona1.Menor();
Persona2.Menor();
Persona1.Edad_En_Dias();
Persona2.Edad_En_Dias();
Persona1.Edad_En_Meses();
Persona2.Edad_En_Meses();

//Crear una función o método que calcule la edad a partir de la fecha de nacimiento.