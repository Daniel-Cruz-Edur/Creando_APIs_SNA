var Weight;
var Height;

var Contesta = 0;
var Acumulador_Height = 0;
var Acumulador_Weight = 0;


function Add_Values()
{
    Weight = parseFloat(prompt('Ingrese su peso: '));
    Height = parseFloat(prompt('Ingrese su altura en metros (Metros): '))
    Contesta++;
    Acumulador_Height += Height;
    Acumulador_Weight += Weight;
}

function Calcular_IMC()
{
    let IMC = Weight / (Height * Height);
    if (IMC < 18.5)
    {
        console.log('Indice de masa corporal: ' + IMC);
        document.write('Clasificación: Bajo Peso. ')
    }
    else if (IMC >= 18.5 && IMC < 25)
    {
        console.log('Indice de masa corporal: ' + IMC);
        document.write('Clasificación: Peso Normal. ')
    }
    else if (IMC >= 25 && IMC < 30)
    {
        console.log('Indice de masa corporal: ' + IMC);
        document.write('Clasificación: Sobrepeso. ')
    }
    else
    {
        console.log('Indice de masa corporal: ' + IMC);
        document.write('Clasificación: Obeso. ')
    }
}

function Pregunta()
{
    var Respuesta = prompt('¿Desea continuar?').toLocaleUpperCase();

    return Respuesta == 'SI' || Respuesta == 'si';
}

function Height_Average()
{
    if (Contesta == 0)
    {
        console.log('No se han ingresado valores. ');
    }
    else
    {
        let Average =  Acumulador_Height/Contesta;
        console.log('El promedio de altura es: ' + Average)
    }
}

function Weight_Average()
{
    if (Contesta == 0)
    {
        console.log('No se han ingresado valores. ');
    }
    else
    {
        let Average =  Acumulador_Weight/Contesta;
        console.log('El promedio de peso es: ' + Average)
    }
}

// Este el el inicio del bucle.
do
    {
        Add_Values();
        Calcular_IMC();
    }
while (Pregunta());

Height_Average();
Weight_Average();